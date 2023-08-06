#ifndef CASCREL_NORMALINITIALIZERPARAM_HPP
#define CASCREL_NORMALINITIALIZERPARAM_HPP

#include "common.hpp"

#include "params/initializers/InitializerParam.hpp"

class NormalInitializerParam : public InitializerParam {
public:
    NormalInitializerParam(cascrel::Scalar mean, cascrel::Scalar std_dev);

    void visit(cascrel::factory::Builder& builder) const override;

    void visitAlternative(cascrel::factory::Builder& builder) const override;
private:
    cascrel::Scalar mMean;
    cascrel::Scalar mStdDev;
};


#endif //CASCREL_NORMALINITIALIZERPARAM_HPP
