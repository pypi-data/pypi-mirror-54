#ifndef CASCREL_LINEARACTIVATIONPARAM_HPP
#define CASCREL_LINEARACTIVATIONPARAM_HPP

#include "params/activation/ActivationParam.hpp"

class LinearActivationParam : public ActivationParam {
public:
    void visit(cascrel::factory::Builder& builder) const override;

    void visitAlternative(cascrel::factory::Builder& builder) const override;
};


#endif //CASCREL_LINEARACTIVATIONPARAM_HPP
