#ifndef PYCASCREL_PARAMETER_HPP
#define PYCASCREL_PARAMETER_HPP

#include "factory/Builder.hpp"

class Parameter {
public:
    virtual void visit(cascrel::factory::Builder& builder) const = 0;

    virtual void visitAlternative(cascrel::factory::Builder& builder) const {}
};

#endif //PYCASCREL_PARAMETER_HPP
