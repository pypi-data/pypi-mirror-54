#ifndef CASCREL_HYPERBOLICTANGENTACTIVATIONPARAM_HPP
#define CASCREL_HYPERBOLICTANGENTACTIVATIONPARAM_HPP

#include "params/activation/ActivationParam.hpp"

class HyperbolicTangentActivationParam : public ActivationParam {
public:
    void visit(cascrel::factory::Builder& builder) const override;

    void visitAlternative(cascrel::factory::Builder& builder) const override;
};


#endif //CASCREL_HYPERBOLICTANGENTACTIVATIONPARAM_HPP
