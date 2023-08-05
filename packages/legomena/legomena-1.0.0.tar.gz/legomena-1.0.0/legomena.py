# bloody dependencies
from collections import Counter, namedtuple
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import fsolve, curve_fit
from scipy.special import comb as nCr
from scipy.stats import linregress


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent


def get_data_path() -> Path:
    """Returns project data folder."""
    return get_project_root() / "data"


class HeapsModel:
    """Heap's Law: Types = K*Tokens^B"""

    # params
    HeapsParams = namedtuple("HeapsParams", ("K", "B"))
    _params = None

    @property
    def params(self) -> tuple:  # HeapsParams
        assert (
            self._params is not None
        ), "Please use .fit(m_tokens, n_types) to fit the model."
        return self._params

    @params.setter
    def params(self, params_: tuple):
        self._params = self.HeapsParams(*params_)

    @property
    def K(self) -> int:
        """Heap's Law coefficient K."""
        return self.params.K

    @property
    def B(self) -> int:
        """Heap's Law exponent B."""
        return self.params.B

    def fit(self, m_tokens: np.ndarray, n_types: np.ndarray):
        """
        Naive fit: Linear regression on logN = B*logM + expK
        :param m_tokens: Number of tokens, list-like independent variable
        :param n_types: Number of types, list-like dependent variable
        :returns: (self) Fitted model
        """

        # convert to log/log
        log_m = np.log(m_tokens)
        log_n = np.log(n_types)
        slope, intercept, r_value, p_value, std_err = linregress(x=log_m, y=log_n)
        K = np.exp(intercept)
        B = slope
        self.params = (K, B)

        # return fitted model
        return self

    def predict(self, m_tokens: np.ndarray, nearest_int: bool = True) -> np.ndarray:
        """
        Calculate & return n_types = E(m_tokens) = Km^B
        :param m_tokens: Number of tokens, list-like independent variable
        :param nearest_int: (bool, True) Round predictions to the nearest integer
        :returns: Number of types as predicted by Heap's Law
        """

        # allow scalar
        return_scalar = np.isscalar(m_tokens)
        m_tokens = np.array(m_tokens).reshape(-1)

        # run model
        K, B = self.params
        n_types = K * np.power(m_tokens, B)
        if nearest_int:
            n_types = np.round(n_types)

        # allow scalar
        if return_scalar:
            assert len(n_types) == 1
            n_types = n_types[0]

        # return
        return n_types

    def fit_predict(self, m_tokens: np.ndarray, n_types: np.ndarray) -> np.ndarray:
        """
        Equivalent to fit(m_tokens, n_types).predict(m_tokens)
        :param m_tokens: Number of tokens, list-like independent variable
        :param n_types: Number of types, list-like dependent variable
        :returns: Number of types as predicted by Heap's Law
        """

        # fit and predict
        return self.fit(m_tokens, n_types).predict(m_tokens)


class LogModel:
    """Types = N_z * ln(Tokens/M_z) * Tokens/M_z / (Tokens/M_z - 1)"""

    # params
    LogParams = namedtuple("LogParams", ("M_z", "N_z"))
    _params = None

    # user options
    UserOptions = namedtuple("UserOptions", ("epsilon", "dimension"))
    _options = UserOptions(
        epsilon=1e-3,  # distance to singularity to return limiting value
        dimension=6,  # max value of n returned for n-legomena count prediction
    )

    @property
    def params(self) -> tuple:  # LogParams
        assert (
            self._params is not None
        ), "Please use .fit(m_tokens, n_types) to fit the model."
        return self._params

    @params.setter
    def params(self, params_: tuple):
        self._params = self.LogParams(*params_)

    @property
    def M_z(self) -> int:
        """The number of tokens in this corpus's optimum sample."""
        return self.params.M_z

    @property
    def N_z(self) -> int:
        """The number of types in this corpus's optimum sample."""
        return self.params.N_z

    @property
    def options(self) -> tuple:  # UserOptions
        """Misc low-impact options when evaluating the log formula."""
        return self._options

    @options.setter
    def options(self, opt_: tuple):
        opt_ = self.UserOptions(*opt_)
        dim = opt_.dim
        assert dim <= 6, "Cannot predict n-legomena counts for n > 6 at this time."
        self._options = opt_

    @property
    def epsilon(self) -> float:
        """Distance to singularity to return limiting value."""
        return self.options.epsilon

    @epsilon.setter
    def epsilon(self, eps_: int):
        eps, dim = self.options
        eps = eps_
        self.options = (eps, dim)

    @property
    def dimension(self) -> int:
        """Max value of n returned for n-legomena count prediction."""
        return self.options.dimension

    @dimension.setter
    def dimension(self, dim_: int):
        eps, dim = self.options
        dim = dim_
        self.options = (eps, dim)

    def formula(self, x: np.ndarray) -> np.ndarray:
        """
        Predicts normalized k-vector for given proportion of tokens.
        NOTE: Eqns (17.*) in https://arxiv.org/pdf/1901.00521.pdf
        :param x: List-like independent variable x, the proportion of tokens
        :returns k_frac: Expected proportions of n-legomena for n = 0 to dim
        """

        x = np.array(x).reshape(-1)

        # TODO: implement generalized formula
        epsilon = self.options.epsilon
        dim = self.options.dimension

        # initialize return vectors
        _k_frac = np.zeros((len(x), dim))

        # two singularities @ x=0 & x=1
        x_iszero = np.abs(x) < epsilon  # singularity @ x=0
        x_isone = np.abs(x - 1.0) < epsilon  # singularity @ x=1
        x_isokay = ~np.logical_or(x_iszero, x_isone)
        x = x[x_isokay]

        # initialize results
        k_frac = np.zeros((len(x), dim))
        logx = np.log(x)
        x2, x3, x4, x5, x6 = [x ** i for i in range(2, dim + 1)]
        k_frac[:, 0] = (x - logx * x - 1) / (x - 1)
        k_frac[:, 1] = (x2 - logx * x - x) / (x - 1) ** 2
        k_frac[:, 2] = (x3 - 2 * logx * x2 - x) / 2 / (x - 1) ** 3
        k_frac[:, 3] = (2 * x4 - 6 * logx * x3 + 3 * x3 - 6 * x2 + x) / 6 / (x - 1) ** 4
        k_frac[:, 4] = (
            (3 * x5 - 12 * logx * x4 + 10 * x4 - 18 * x3 + 6 * x2 - x)
            / 12
            / (x - 1) ** 5
        )
        k_frac[:, 5] = (
            (12 * x6 - 60 * logx * x5 + 65 * x5 - 120 * x4 + 60 * x3 - 20 * x2 + 3 * x)
            / 60
            / (x - 1) ** 6
        )

        # limiting values @ x=0 & x=1
        _k_frac[x_iszero, :] = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        _k_frac[x_isone, :] = np.array(
            [0.0, 1.0 / 2, 1.0 / 6, 1.0 / 12, 1.0 / 20, 1.0 / 30]
        )
        _k_frac[x_isokay] = k_frac

        # return proportions
        return _k_frac

    def fit_naive(self, m_tokens: int, n_types: int, h_hapax: int):
        """
        Uses observed whole-corpus hapax:type ratio to infer M_z, N_z optimum sample size.
        :param m_tokens: (int, scalar) Number of tokens in the corpus.
        :param n_types: (int, scalar) Number of types in the corpus.
        :param h_hapax: (int, scalar) Number of hapax in the corpus.
        :returns: (self) Fitted model
        """

        # infer z from h_obs
        h_obs = h_hapax / n_types  # observed hapax proportion
        func = lambda x: 1.0 / np.log(x) + 1.0 / (1.0 - x) - h_obs
        z0 = 0.5
        z = fsolve(func, z0)[0]
        M_z = m_tokens / z
        N_z = n_types * (z - 1) / z / np.log(z)
        M_z, N_z = int(M_z), int(N_z)
        self.params = (M_z, N_z)

        # return fitted model
        return self

    def fit(self, m_tokens: np.ndarray, n_types: np.ndarray):
        """
        Uses scipy.optimize.curve_fit() to fit the log model to type-token data.
        :param m_tokens: Number of tokens, list-like independent variable
        :param n_types: Number of types, list-like dependent variable
        :returns: (self) Fitted model
        """

        # initial guess: naive fit
        M, N, H = max(m_tokens), max(n_types), max(n_types) / 2
        p0 = self.fit_naive(M, N, H).params

        # minimize MSE on random perturbations of M_z, N_z
        func = lambda m, M_z, N_z: N_z * np.log(m / M_z) * m / M_z / (m / M_z - 1)
        xdata = np.array(m_tokens)
        ydata = np.array(n_types)
        params_, _ = curve_fit(func, xdata, ydata, p0)
        M_z, N_z = params_.astype("int")
        self.params = (M_z, N_z)

        # return fitted model
        return self

    def predict(self, m_tokens: np.ndarray, nearest_int: bool = True) -> np.ndarray:
        """
        Calculate & return n_types = N_z * formula(m_tokens/M_z)
        NOTE: predict(m) == N_z - predict_k(m)[0]
        :param m_tokens: Number of tokens, list-like independent variable
        :param nearest_int: (bool, True) Round predictions to the nearest integer
        :returns: Number of types as predicted by logarithmic model.
        """

        # allow scalar
        return_scalar = np.isscalar(m_tokens)
        m_tokens = np.array(m_tokens).reshape(-1)

        # redirect: E(m) = N_z - k_0(m)
        k = self.predict_k(m_tokens, nearest_int=nearest_int)
        n_types = self.N_z - k[:, 0]

        # allow scalar
        if return_scalar:
            assert len(n_types) == 1
            n_types = float(n_types)

        # return number of types
        return n_types

    def predict_k(
        self, m_tokens: np.ndarray, normalize: bool = False, nearest_int: bool = True
    ) -> np.ndarray:
        """
        Applies the log formula to model the k-vector as a function of tokens.
        :param m_tokens: Number of tokens (scalar or list-like)
        :param normalize: (bool, False) Return proportions instead of counts
        :param nearest_int: (bool, True) Round predictions to the nearest integer
        :returns k: Predicted n-legomena counts for n = 0 to 5
        """

        # allow scalar
        return_scalar = np.isscalar(m_tokens)
        m_tokens = np.array(m_tokens).reshape(-1)

        # retrieve fitting parameters
        M_z, N_z = self.params

        # scale down to normalized log formula
        x = m_tokens / M_z
        k_frac = self.formula(x)

        # normalize, or don't
        if normalize:
            # predicted counts as a proportion of predicted types
            y_types_omitted = k_frac[:, 0]
            y_types_selected = 1 - y_types_omitted
            y_types_selected = y_types_selected[:, np.newaxis]
            k = k_frac / y_types_selected
        else:
            # predicted counts
            k = N_z * k_frac
            if nearest_int:
                k = np.round(k)

        # allow scalar
        if return_scalar:
            assert len(k) == 1
            k = k.squeeze()

        # return n-legomena counts
        return k

    def fit_predict(self, m_tokens: np.ndarray, n_types: np.ndarray) -> np.ndarray:
        """
        Equivalent to fit(m_tokens, n_types).predict(m_tokens)
        :param m_tokens: Number of tokens, list-like independent variable
        :param n_types: Number of types, list-like dependent variable
        :returns: Number of types as predicted by logarithmic model
        """

        # fit and predict
        return self.fit(m_tokens, n_types).predict(m_tokens)


class Corpus(Counter):
    """Wrapper class for bag of words text model."""

    # object properties
    _k = None  # k-vector of n-legomena counts
    _TTR = None  # dataframe containing type/token counts from corpus samples
    _tokens = None  # memoized list of tokens
    _types = None  # memoized list of types

    # user options
    UserOptions = namedtuple("UserOptions", ("resolution", "dimension", "seed"))
    _options = UserOptions(
        resolution=100,  # number of samples to take when building a TTR curve
        dimension=7,  # vector size for holding n-legomena counts (zero-based)
        seed=None,  # random number seed for taking samples when building TTR
    )

    @property
    def tokens(self) -> list:
        """The bag of words, list-like of elements of any type."""
        if self._tokens is None:
            tokens_ = sorted(list(self.elements()))
            self._tokens = tokens_
        return self._tokens

    @property
    def types(self) -> list:
        """The lexicon, ranked by frequency."""
        if self._types is None:
            fdist = self.fdist  # ranked order
            types_ = list(fdist.type.values)
            self._types = types_
        return self._types

    @property
    def fdist(self) -> pd.DataFrame:
        """The frequency distribution, as a dataframe."""
        df = pd.DataFrame.from_dict(self, orient="index").reset_index()
        df.columns = ["type", "freq"]
        df = df.sort_values("freq", ascending=False).reset_index(drop=True)
        df.index = df.index + 1
        df.index.name = "rank"
        return df

    @property
    def WFD(self) -> pd.DataFrame:
        """Word Frequency Distribution, as a dataframe."""
        return self.fdist

    @property
    def k(self) -> np.ndarray:
        """The vector describing the frequency of n-legomena."""
        if self._k is None:
            self._k = Counter(self.values())

        # return as array
        k = self._k
        kmax = max(k.keys())
        karr = np.array([k[i] for i in range(kmax + 1)])
        return karr

    @property
    def M(self) -> int:
        """The number of tokens in the corpus."""
        m_tokens = sum(self.values())
        return m_tokens

    @property
    def N(self) -> int:
        """The number of types in the corpus."""
        n_types = len(self)
        return n_types

    @property
    def options(self) -> tuple:  # UserOptions
        """Misc low-impact options when computing the TTR curve."""
        return self._options

    @options.setter
    def options(self, opt_: tuple):
        self._options = self.UserOptions(*opt_)
        self._TTR = None
        self._params = None

    @property
    def resolution(self) -> int:
        """The desired resolution (number of samples) of the TTR curve."""
        return self.options.resolution

    @resolution.setter
    def resolution(self, res_: int):
        res, dim, seed = self.options
        res = res_
        self.options = (res, dim, seed)

    @property
    def dimension(self) -> int:
        """The desired dimension of the problem, highest n for which n-legomena counts are included in TTR."""
        return self.options.dimension

    @dimension.setter
    def dimension(self, dim_: int):
        res, dim, seed = self.options
        dim = dim_
        self.options = (res, dim, seed)

    @property
    def seed(self) -> int:
        """Random number seed."""
        return self.options.seed

    @seed.setter
    def seed(self, seed_: int):
        res, dim, seed = self.options
        seed = seed_
        self.options = (res, dim, seed)

    @property
    def TTR(self) -> pd.DataFrame:
        """DataFrame of type-token relation data."""
        if self._TTR is None:
            self._TTR = self._compute_TTR()
        return self._TTR.copy()

    #
    def nlegomena(self, n: int) -> list:
        """List of types occurring exactly n times in the corpus."""
        nlegomena_ = [typ for typ, freq in self.items() if freq == n]
        return nlegomena_

    @property
    def hapax(self):
        """List of hapax (words that appear exactly once)"""
        return self.nlegomena(1)

    @property
    def dis(self):
        """List of dis legomena (words that appear exactly twice)"""
        return self.nlegomena(2)

    @property
    def tris(self):
        """List of tris legomena (words that appear exactly three times)"""
        return self.nlegomena(3)

    @property
    def tetrakis(self):
        """List of tetrakis legomena (words that appear exactly four times)"""
        return self.nlegomena(4)

    @property
    def pentakis(self):
        """List of pentakis legomena (words that appear exactly five times)"""
        return self.nlegomena(5)

    def as_datarow(self, dim: int) -> tuple:
        """Formats corpus metadata as (M, N, k[0], k[1], ... k[dim])"""
        as_tuple = (self.M, self.N)
        as_tuple += tuple(self.k[:dim])
        return as_tuple

    #
    def sample(self, m: int = None, x: float = None):
        """
        Samples either <m> tokens or <x> proportion of tokens and returns smaller Corpus.
        :param m: (int) Number of tokens to sample *without replacement*. (m <= M)
        :param x: (float) Proportion of corpus to sample. (x <= 1)
        :returns: Corpus composed of sampled tokens.
        """

        # sample
        m = m or int(x * self.M)
        seed = self.seed
        if seed:
            seed = seed + m  # salt
        random_state = np.random.RandomState(seed)
        tokens = random_state.choice(self.tokens, m, replace=False)
        corpus = Corpus(tokens)
        return corpus

    #
    def _compute_TTR(self) -> pd.DataFrame:
        """
        Samples the corpus at intervals 1/res, 2/res, ... 1 to build a Type-Token Relation
        curve consisting of <resolution> points <(m, n)>
        :returns: Dataframe of token/type/legomena counts
        """

        # user options
        res, dim, seed = self.options

        # sample the corpus
        x_choices = (np.arange(res) + 1) / res
        TTR = [self.sample(x=x).as_datarow(dim) for x in x_choices]

        # save to self.TTR as dataframe
        colnames = ["m_tokens", "n_types"]
        if dim is not None:
            colnames += ["lego_" + str(x) for x in range(dim)]
        TTR = pd.DataFrame(TTR, columns=colnames)

        # types *not* drawn
        TTR.lego_0 = self.N - TTR.n_types

        # return
        return TTR


class InfSeriesModel:
    """
    Runs infinite series model to predict N = E(M)
    NOTE: Eqn (8b) in https://arxiv.org/pdf/1901.00521.pdf
    """

    def __init__(self, corpus: Corpus):
        """No fit() function, instantiate model as an extension of corpus."""

        # the legomena counts parametrize this model
        self.M = corpus.M
        self.N = corpus.N
        self.k = corpus.k

    def predict(self, m_tokens: np.ndarray, nearest_int: bool = True) -> np.ndarray:
        """
        Calculate & return n_types = E(m_tokens) = Km^B
        :param m_tokens: Number of tokens, list-like independent variable
        :param nearest_int: (bool, True) Round predictions to the nearest integer
        :returns: Number of types as predicted by Heap's Law
        """

        # allow scalar
        return_scalar = np.isscalar(m_tokens)
        m_tokens = np.array(m_tokens).reshape(-1)

        # sum over legomena coefficients k
        x = m_tokens / self.M
        exponents = range(len(self.k))
        terms = np.array([np.power(1 - x, n) for n in exponents])
        k_0 = np.dot(self.k, terms)
        n_types = self.N - k_0
        if nearest_int:
            n_types = np.round(n_types)

        # allow scalar
        if return_scalar:
            assert len(n_types) == 1
            n_types = n_types[0]

        # return
        return n_types


class SPGC:
    """
    Standard Project Gutenberg Corpus
    ---------------------------------
    Created by Font-Clos, F. & Gerlach, M. https://arxiv.org/abs/1812.08092
    Snapshot downloaded from: https://zenodo.org/record/2422561/files/SPGC-counts-2018-07-18.zip
    """

    # counts file
    fcounts = "SPGC-counts-2018-07-18"
    fmeta = "SPGC-metadata-2018-07-18"
    weburl = "https://zenodo.org/record/2422561"

    @classmethod
    def download(cls):
        """
        Downloads SPGC data from weburl
        Extracts it into data/
        """

        # credit: https://svaderia.github.io/articles/downloading-and-unzipping-a-zipfile/
        from io import BytesIO
        from urllib.request import urlopen
        from zipfile import ZipFile

        zipurl = "%s/files/%s.zip" % (cls.weburl, cls.fcounts)
        with urlopen(zipurl) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                data_path = get_data_path()
                zfile.extractall(data_path)

    @classmethod
    def get(cls, pgid: int) -> Corpus:
        """
        Retrieves word frequency distribution for book by PGID
        :param pgid: (int or str) Project Gutenberg book ID, ex get(2701) or get("PG2701")
        :returns: Corpus, wrapper class for the "bag of words" text model
        """

        # convert int -> str
        pgid = str(pgid)
        if pgid[:2] != "PG":
            pgid = "PG%s" % pgid

        # build corpus from frequency distribution
        data_path = get_data_path()
        fname = data_path / cls.fcounts / ("%s_counts.txt" % pgid)
        with fname.open() as f:
            df = pd.read_csv(f, delimiter="\t", header=None, names=["word", "freq"])
            f.close()

        # build corpus
        asdict = {str(row.word): int(row.freq) for row in df.itertuples()}
        corpus = Corpus(asdict)

        # return corpus object
        return corpus

    @classmethod
    def metadata(cls, language: str = None) -> pd.DataFrame:
        """
        Retrieves metadata.csv and returns as dataframe.
        :param language: (optional) 2-letter language code, 'en', 'fr', etc
        """

        # read csv
        data_path = get_data_path()
        fname = data_path / ("%s.csv" % cls.fmeta)
        df = pd.read_csv(fname).set_index("id")
        df = df[~df.title.isna()]

        # strip out "sound" entries
        df = df.query('type == "Text"')
        assert df.shape == (56395, 8), "ERROR: Corrupted SPGC file %s" % fname

        # filter language
        if language is not None:
            language = "['%s']" % language
            df = df.query("language == @language")

        # return
        return df
