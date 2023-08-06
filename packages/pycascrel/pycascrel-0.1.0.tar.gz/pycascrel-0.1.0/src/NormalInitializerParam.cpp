#include "params/initializers/NormalInitializerParam.hpp"

#include "initializers/NormalInitializer.hpp"

using cascrel::initializers::NormalInitializer;

NormalInitializerParam::NormalInitializerParam(cascrel::Scalar mean,
                                               cascrel::Scalar std_dev)
        : mMean(mean),
          mStdDev(std_dev) {
}

void NormalInitializerParam::visit(cascrel::factory::Builder& builder) const {
    builder.withHiddenInitializer<NormalInitializer>(mMean, mStdDev);
}

void NormalInitializerParam::visitAlternative(
        cascrel::factory::Builder& builder) const {
    builder.withOutputInitializer<NormalInitializer>(mMean, mStdDev);
}
