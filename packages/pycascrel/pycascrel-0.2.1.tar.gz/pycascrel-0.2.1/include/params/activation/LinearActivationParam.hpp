#ifndef PYCASCREL_LINEARACTIVATIONPARAM_HPP
#define PYCASCREL_LINEARACTIVATIONPARAM_HPP

#include "params/activation/ActivationParam.hpp"

class LinearActivationParam : public ActivationParam {
public:
    void visit(cascrel::factory::Builder& builder) const override;

    void visitAlternative(cascrel::factory::Builder& builder) const override;
};


#endif //PYCASCREL_LINEARACTIVATIONPARAM_HPP
