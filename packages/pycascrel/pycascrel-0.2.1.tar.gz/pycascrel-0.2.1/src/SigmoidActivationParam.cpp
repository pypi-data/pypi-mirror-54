#include "params/activation/SigmoidActivationParam.hpp"

#include "activation/SigmoidActivation.hpp"

using cascrel::activation::SigmoidActivation;

void SigmoidActivationParam::visit(cascrel::factory::Builder& builder) const {
    builder.withHiddenActivation<SigmoidActivation>();
}

void SigmoidActivationParam::visitAlternative(
        cascrel::factory::Builder& builder) const {
    builder.withOutputActivation<SigmoidActivation>();
}
