# trade_lifecycle/lifecycle_profiles.py


class BaseLifecycleProfile:

    """
    Pure lifecycle interpretation profile.

    Responsibilities:
    - Interpret deterioration behavior
    - Define calm lifecycle thresholds
    - Remain completely isolated from:
        - market prediction
        - signal generation
        - execution authority
    """

    # ==================================================
    # 🔥 INIT
    # ==================================================

    def __init__(self):

        self.profile_name = "BASE"

        # deterioration
        self.max_deterioration = 0.08

        # weakening persistence
        self.max_weak_cycles = 2

        # recovery behavior
        self.recovery_factor = 0.8

        # pullback tolerance
        self.pullback_tolerance = 0.015

        # exit behavior
        self.requires_exit_confirmation = True

        # confidence sensitivity
        self.low_confidence_penalty = True

    # ==================================================
    # 🔥 DETERIORATION EVALUATION
    # ==================================================

    def should_start_exit_watch(
        self,
        trade_object
    ):

        if (
            trade_object.deterioration_score
            >= self.max_deterioration
        ):
            return True

        if (
            trade_object.consecutive_weak_cycles
            >= self.max_weak_cycles
        ):
            return True

        return False

    # ==================================================
    # 🔥 EXIT CONFIRMATION
    # ==================================================

    def should_confirm_exit(
        self,
        trade_object
    ):

        if not trade_object.exit_pending:
            return False

        if (
            trade_object.consecutive_weak_cycles
            >= self.max_weak_cycles
        ):
            return True

        return False

    # ==================================================
    # 🔥 RECOVERY
    # ==================================================

    def apply_recovery_decay(
        self,
        deterioration_score
    ):

        return (
            deterioration_score
            * self.recovery_factor
        )


# ======================================================
# 🔥 RANGE PROFILE
# ======================================================

class RangeLifecycleProfile(
    BaseLifecycleProfile
):

    """
    Fast invalidation profile.

    Designed for:
    - fragile structures
    - short-lived balance
    - fast rejection detection
    - rapid deterioration response
    """

    def __init__(self):

        super().__init__()

        self.profile_name = "RANGE"

        # range trades collapse faster
        self.max_deterioration = 0.045

        # react faster to weakness
        self.max_weak_cycles = 1

        # recover slower
        self.recovery_factor = 0.9

        # tighter tolerance
        self.pullback_tolerance = 0.01

        self.requires_exit_confirmation = True

        self.low_confidence_penalty = True


# ======================================================
# 🔥 TREND PROFILE
# ======================================================

class TrendLifecycleProfile(
    BaseLifecycleProfile
):

    """
    Calm continuation profile.

    Designed for:
    - pullback tolerance
    - continuation persistence
    - slower deterioration
    - institutional trend holding
    """

    def __init__(self):

        super().__init__()

        self.profile_name = "TREND"

        # tolerate more deterioration
        self.max_deterioration = 0.12

        # allow continuation fluctuations
        self.max_weak_cycles = 3

        # recover faster
        self.recovery_factor = 0.65

        # wider tolerance
        self.pullback_tolerance = 0.03

        self.requires_exit_confirmation = True

        self.low_confidence_penalty = False


# ======================================================
# 🔥 PROFILE FACTORY
# ======================================================

def get_lifecycle_profile(
    trade_type
):

    if trade_type == "RANGE":

        return RangeLifecycleProfile()

    return TrendLifecycleProfile()
