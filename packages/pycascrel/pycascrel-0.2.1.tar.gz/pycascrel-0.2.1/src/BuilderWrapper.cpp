#include "BuilderWrapper.hpp"

using cascrel::SizeType;

void BuilderWrapper::useHiddenInitializer(const InitializerParam& p) {
    p.visit(mBuilder);
}

void BuilderWrapper::useOutputInitializer(const InitializerParam& p) {
    p.visitAlternative(mBuilder);
}

void BuilderWrapper::useHiddenOptimizer(const OptimizerParam& p) {
    p.visit(mBuilder);
}

void BuilderWrapper::useOutputOptimizer(const OptimizerParam& p) {
    p.visitAlternative(mBuilder);
}

void BuilderWrapper::useHiddenActivation(const ActivationParam& p) {
    p.visit(mBuilder);
}

void BuilderWrapper::useOutputActivation(const ActivationParam& p) {
    p.visitAlternative(mBuilder);
}

void BuilderWrapper::useLoss(const LossParam& p) {
    p.visit(mBuilder);
}

CascadeCorrelationNetworkWrapper
BuilderWrapper::compile(SizeType inputDimension, SizeType outputDimension) {
    return CascadeCorrelationNetworkWrapper(
            mBuilder.buildWithDimensions(inputDimension, outputDimension));
}
