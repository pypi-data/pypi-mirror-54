#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "common.hpp"

#include "BuilderWrapper.hpp"
#include "CascadeCorrelationNetworkWrapper.hpp"
#include "HiddenHistory.hpp"
#include "History.hpp"
#include "params/activation/HyperbolicTangentActivationParam.hpp"
#include "params/activation/LinearActivationParam.hpp"
#include "params/activation/SigmoidActivationParam.hpp"
#include "params/activation/SoftplusActivationParam.hpp"
#include "params/initializers/NormalInitializerParam.hpp"
#include "params/loss/MeanSquareLossParam.hpp"
#include "params/optimizers/DeltaRuleOptimizerParam.hpp"

namespace py = pybind11;

using namespace py::literals;

using cascrel::Scalar;

PYBIND11_MODULE(pycascrel, m) {
    m.doc() = R"pbdoc(
        pycascrel API reference
        =======================

        The Cascade-Correlation method framework programming reference.

        Modules
        -------

        These modules provide various components of the CCN network
        as classes that can be passed to various CcnBuilder methods.

        .. autosummary::
           :toctree: _generate

           loss
           initializers
           optimizers
           activation

        Members
        -------
        .. autosummary::
           :toctree: _generate
           :template: class.rst

           LogLevel
           History
           HiddenHistory
           CcnBuilder
           CascadeCorrelationNetwork
    )pbdoc";

    // loss module
    auto mloss = m.def_submodule("loss", R"pbdoc(
    Components providing different loss functions.

    .. autosummary::
       :toctree: _generate
       :template: class.rst

       MeanSquare
)pbdoc");

    py::class_<LossParam>(mloss, "Loss");

    py::class_<MeanSquareLossParam, LossParam>(mloss, "MeanSquare", R"pbdoc(
    Transforms network output loss (difference between response and target output values)
    in order to form an optimizable function.

    The loss value :math:`e` is transformed as such:

    .. math::
       f(e) = \frac{1}{2} e^2
)pbdoc")
            .def(py::init<>());

    // initializers module
    auto minitializers = m.def_submodule("initializers", R"pbdoc(
    Components providing ways of initializing layers.

    .. autosummary::
       :toctree: _generate
       :template: class.rst

       Normal
)pbdoc");

    py::class_<InitializerParam>(minitializers, "Initializer");

    py::class_<NormalInitializerParam, InitializerParam>(
            minitializers, "Normal", R"pbdoc(
    Assigns consecutive initialized elements pseudorandom values
    from a normal (Gauss) distribution.
)pbdoc")
            .def(py::init<Scalar, Scalar>(),
                 "mean"_a = 0., "std_dev"_a = 1., py::doc(R"pbdoc(
    Create a new initializer with the specified params.

    Args:
        mean (float): mean value of the distribution
        std_dev (float): standard deviation of the distribution
)pbdoc"));

    // optimizers module
    auto moptimizers = m.def_submodule("optimizers", R"pbdoc(
    Components providing optimization for various network learning stages.

    .. autosummary::
       :toctree: _generate
       :template: class.rst

       DeltaRule
)pbdoc");

    py::class_<OptimizerParam>(moptimizers, "Optimizer");

    py::class_<DeltaRuleOptimizerParam, OptimizerParam>(
            moptimizers, "DeltaRule", R"pbdoc(
    A simple delta rule optimization algorithm.
)pbdoc")
            .def(py::init<Scalar>(), "learning_rate"_a = 0.01, py::doc(R"pbdoc(
    Initialize the algorithm.

    Args:
        learning_rate (float): learning rate, this value is multiplied
            by the optimization result to control learning speed
)pbdoc"));

    // activation module
    auto mactivation = m.def_submodule("activation", R"pbdoc(
    Components providing activation for individual network layers.

    .. autosummary::
       :toctree: _generate

       TanH
       Linear
       Sigmoid
       Softplus
)pbdoc");

    py::class_<ActivationParam>(mactivation, "Activation");

    py::class_<HyperbolicTangentActivationParam, ActivationParam>(
            mactivation, "TanH", R"pbdoc(
    Hyperbolic tangent activation function.
)pbdoc")
            .def(py::init<>());

    py::class_<LinearActivationParam, ActivationParam>(
            mactivation, "Linear", R"pbdoc(
    Linear activation function.
)pbdoc")
            .def(py::init<>());

    py::class_<SigmoidActivationParam, ActivationParam>(
            mactivation, "Sigmoid", R"pbdoc(
    Sigmoid activation function.
)pbdoc")
            .def(py::init<>());

    py::class_<SoftplusActivationParam, ActivationParam>(
            mactivation, "Softplus", R"pbdoc(
    Softplus activation function.
)pbdoc")
            .def(py::init<>());

    // main module
    py::enum_<cascrel::LogLevel>(m, "LogLevel", R"pbdoc(
    A flag for setting log output verbosity level
    as described below.
)pbdoc")
            .value("DEBUG", cascrel::LogLevel::DEBUG, R"pbdoc(
    Additional debug info is shown.
)pbdoc")
            .value("INFO", cascrel::LogLevel::INFO, R"pbdoc(
    Standard user facing logs. This is the default log setting.
)pbdoc")
            .value("WARN", cascrel::LogLevel::WARN, R"pbdoc(
    Only warnings are shown.
)pbdoc")
            .value("OFF", cascrel::LogLevel::OFF, R"pbdoc(
    All logs are disabled.
)pbdoc")
            .export_values();

    py::class_<cascrel::HiddenHistory>(m, "HiddenHistory", R"pbdoc(
    Contains the history of learning statistics for a single hidden network layer.
)pbdoc")
            .def("get_covariance_records", &cascrel::HiddenHistory::getCovarianceRecords, py::doc(R"pbdoc(
    Represents mean covariance values between a hidden layer and the network outputs.
)pbdoc"));

    py::class_<cascrel::History>(m, "History", R"pbdoc(
    Contains the history of various learning statistics over all training epochs.

    The returned statistics are lists of data suitable to present as
    matplotlib plots, i.e. consecutive values correspond to consecutive epochs,
    e.g. :code:`arr[0]` is the value for the first epoch,
    :code:`arr[1]` is the value for the second epoch, and so on.
)pbdoc")
            .def("get_loss_records", &cascrel::History::getLossRecords, py::doc(R"pbdoc(
    Represents mean loss value of all network outputs over time.
)pbdoc"))
            .def("get_hidden_counts", &cascrel::History::getHiddenCounts, py::doc(R"pbdoc(
    Represents the number of hidden layers connected to the network over time.
)pbdoc"))
            .def("get_hidden_histories", &cascrel::History::getHiddenHistories, py::doc(R"pbdoc(
    A list of :py:class:`pycascrel.HiddenHistory` objects containing training records for individual
    hidden layers in the network.
)pbdoc"));

    py::class_<CascadeCorrelationNetworkWrapper>(m, "CascadeCorrelationNetwork", R"pbdoc(
    Represents a single trainable instance of the CCN network.

    During runtime output is printed to stderr according to the configured log level.
)pbdoc")
            .def("train", &CascadeCorrelationNetworkWrapper::train,
                 "x"_a, "y"_a,
                 "patience"_a = 500, "tolerance"_a = 0.000001,
                 "max_hidden"_a = 20, "max_loss"_a = 0.1,
                 "safety_epoch_limit"_a = 0,
                 py::doc(R"pbdoc(
    Train the network with the specified parameters.

    Args:
        x (np.array): input to train the network on
        y (np.array): target output values for the input
        patience (int): patience
        tolerance (float): tolerance
        max_hidden (int): max hidden
        max_loss (float): max loss
        safety_epoch_limit (int): safety (default 0)

    Returns:
        pycascrel.History: object containing various training statistics
)pbdoc"))
            .def("evaluate", &CascadeCorrelationNetworkWrapper::evaluate,
                 "x"_a, "y"_a, py::doc(R"pbdoc(
    Evaluate mean error in the network using test data.

    Args:
        x (np.array): input to evaluate the network on
        y (np.array): target output values for the input
)pbdoc"))
            .def("predict", &CascadeCorrelationNetworkWrapper::predict, "x"_a, py::doc(R"pbdoc(
    Use the trained network to predict classification values from an unknown input.

    Args:
        x (np.array): Input data to predict from
)pbdoc"))
            .def("get_num_hidden",
                 &CascadeCorrelationNetworkWrapper::getNumHidden, py::doc(R"pbdoc(
    Returns the number of hidden layers in the network after training.

    Returns:
        int: number of hidden layers present in the network
)pbdoc"))
            .def("set_log_level",
                 &CascadeCorrelationNetworkWrapper::setLogLevel, py::doc(R"pbdoc(
    Set the network's log level. See :py:class:`pycascrel.LogLevel` for more information.
)pbdoc"));

    py::class_<BuilderWrapper>(m, "CcnBuilder", R"pbdoc(
    A builder object that allows to conveniently select and setup
    various network components.
)pbdoc")
            .def(py::init<>())
            .def("use_hidden_initializer",
                 &BuilderWrapper::useHiddenInitializer, py::doc(R"pbdoc(
    Specifies an initializer to be used for hidden layers of the network.
)pbdoc"))
            .def("use_output_initializer",
                 &BuilderWrapper::useOutputInitializer, py::doc(R"pbdoc(
    Specifies an initializer to be used for the output layer of the network.
)pbdoc"))
            .def("use_hidden_optimizer", &BuilderWrapper::useHiddenOptimizer, py::doc(R"pbdoc(
    Specifies an optimizer to be used for hidden layers of the network.
)pbdoc"))
            .def("use_output_optimizer", &BuilderWrapper::useOutputOptimizer, py::doc(R"pbdoc(
    Specifies an optimizer to be used for the output layer of the network.
)pbdoc"))
            .def("use_hidden_activation", &BuilderWrapper::useHiddenActivation, py::doc(R"pbdoc(
    Specifies an activation function to be used for hidden layers of the network.
)pbdoc"))
            .def("use_output_activation", &BuilderWrapper::useOutputActivation, py::doc(R"pbdoc(
    Specifies an activation function to be used for the output layer of the network.
)pbdoc"))
            .def("use_loss", &BuilderWrapper::useLoss, py::doc(R"pbdoc(
    Specifies a loss function to be used in the network.
)pbdoc"))
            .def("compile", &BuilderWrapper::compile, py::doc(R"pbdoc(
    Applies selected components (or defaults if unspecified) to the network,
    assigns the specified dimensions
    and returns an instance of the network, ready to work with.

    Args:
        in_dim (int): input size, i.e. number of elements in a single input sample
        out_dim (int): output_size, i.e. number of elements in a single network response to a given sample

    Returns:
        pycascrel.CascadeCorrelationNetwork: a new instance of the network, setup according to the builder specification
)pbdoc"));
}
