#include "params/activation/LinearActivationParam.hpp"

#include "activation/LinearActivation.hpp"

using cascrel::activation::LinearActivation;

void LinearActivationParam::visit(cascrel::factory::Builder& builder) const {
    builder.withHiddenActivation<LinearActivation>();
}

void LinearActivationParam::visitAlternative(
        cascrel::factory::Builder& builder) const {
    builder.withOutputActivation<LinearActivation>();
}
