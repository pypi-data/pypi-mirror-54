"""https://docs.dask.org/en/latest/"""

try:
    from dask import compute, delayed
    from dask.dataframe import from_pandas
    from dask.distributed import Client, as_completed as dask_as_completed
except ImportError:
    compute = None
    delayed = None
    Client = None
    dask_as_completed = None
import pandas as pd
import numpy as np
from tlbx import st, set_missing_key

from glide.core import Node, PushNode, FuturesPush, ParaGlider, PoolSubmit, Reduce
from glide.utils import dbg, is_pandas


class DaskClientPush(FuturesPush):
    """Use a dask Client to do a parallel push"""

    executor_class = Client
    as_completed_func = dask_as_completed

    def run(self, *args, **kwargs):
        assert Client, "Please install dask (Client) to use DaskClientPush"
        super().run(*args, **kwargs)


class DaskDelayedPush(PushNode):
    """Use dask delayed to do a parallel push"""

    def _push(self, item):
        assert delayed, "Please install dask (delayed) to use DaskDelayedPush"

        if self._logging == "output":
            self._write_log(item)

        assert "executor_kwargs" not in self.context, (
            "%s does not currently support executor_kwargs" % self.__class__
        )

        lazy = []
        if self.context.get("split", False):
            splits = np.array_split(item, len(self._downstream_nodes))
            for i, downstream in enumerate(self._downstream_nodes):
                lazy.append(delayed(downstream._process)(splits[i]))
        else:
            for downstream in self._downstream_nodes:
                lazy.append(delayed(downstream._process)(item))

        compute(lazy)


class DaskParaGlider(ParaGlider):
    """A ParaGlider that uses a dask Client to execute parallel calls to
    consume()"""

    def get_executor(self):
        assert Client, "Please install dask (Client) to use DaskParaGlider"
        return Client(**self.executor_kwargs)

    def get_worker_count(self, executor):
        return len(executor.ncores())

    def get_results(self, futures, timeout=None):
        assert not timeout, "timeout argument is not supported for Dask Client"
        dfs = []
        for _, result in dask_as_completed(futures, with_results=True):
            dfs.append(result)
        return dfs


class DaskClientMap(PoolSubmit):
    """Apply a transform to a Pandas DataFrame using dask Client"""

    def check_data(self, data):
        assert is_pandas(data), "DaskClientMap expects a Pandas object, got %s" % type(
            data
        )

    def get_executor(self, **executor_kwargs):
        assert Client, "The dask (Client) package is not installed"
        return Client(**executor_kwargs)

    def get_worker_count(self, executor):
        return len(executor.ncores())

    def submit(self, executor, func, splits, **kwargs):
        futures = executor.map(func, splits, **kwargs)
        return futures

    def get_results(self, futures, timeout=None):
        assert not timeout, "timeout argument is not supported for Dask Client"
        dfs = []
        for _, result in dask_as_completed(futures, with_results=True):
            dfs.append(result)
        return pd.concat(dfs)

    def shutdown_executor(self, executor):
        executor.close()


class DaskFuturesReduce(Reduce):
    """Collect the asynchronous results before pushing"""

    def end(self):
        """Do the push once all Futures results are in.

        Warnings
        --------
        Dask futures will not work if you have closed your client connection!

        """
        dbg("Waiting for %d Dask futures..." % len(self.results))
        results = []
        for _, result in dask_as_completed(self.results, with_results=True):
            results.append(result)
        if self.context.get("flatten", False):
            results = pd.concat(results)
        self.push(results)


class DaskDataFrameApply(Node):
    """Apply a transform to a Pandas DataFrame using dask dataframe"""

    def run(self, df, func, from_pandas_kwargs=None, **kwargs):
        """Convert to dask dataframe and use apply()

        NOTE: it may be more efficient to not convert to/from Dask Dataframe
        in this manner depending on the pipeline

        Parameters
        ----------
        df : pandas.DataFrame
            The pandas DataFrame to apply func to
        func : callable
            A callable that will be passed to Dask DataFrame.apply
        from_pandas_kwargs : optional
            Keyword arguments to pass to dask.dataframe.from_pandas
        **kwargs
            Keyword arguments passed to Dask DataFrame.apply

        """
        assert from_pandas, "The dask (dataframe) package is not installed"
        from_pandas_kwargs = from_pandas_kwargs or {}
        set_missing_key(from_pandas_kwargs, "chunksize", 500)
        set_missing_key(from_pandas_kwargs, "sort", False)
        ddf = from_pandas(df, **from_pandas_kwargs)
        for column in ddf.columns:
            ddf[column] = ddf[column].apply(
                func, meta=(column, ddf[column].dtype), **kwargs
            )
        df = ddf.compute()
        self.push(df)
