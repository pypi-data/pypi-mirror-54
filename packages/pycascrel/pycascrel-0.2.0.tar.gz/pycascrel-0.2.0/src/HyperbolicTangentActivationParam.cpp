#include "params/activation/HyperbolicTangentActivationParam.hpp"

#include "activation/HyperbolicTangentActivation.hpp"

using cascrel::activation::HyperbolicTangentActivation;

void HyperbolicTangentActivationParam::visit(
        cascrel::factory::Builder& builder) const {
    builder.withHiddenActivation<HyperbolicTangentActivation>();
}

void HyperbolicTangentActivationParam::visitAlternative(
        cascrel::factory::Builder& builder) const {
    builder.withOutputActivation<HyperbolicTangentActivation>();
}
