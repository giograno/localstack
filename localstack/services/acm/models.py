from typing import Dict, List

from localstack.services.stores import (
    AccountRegionBundle,
    BaseStore,
    CrossRegionAttribute,
    LocalAttribute,
)

class AcmDummyStore(BaseStore):

    attribute_one: Dict[str, List[Dict]] = LocalAttribute(default=dict)
    # attribute_two: Dict[str, List[Dict]] = LocalAttribute(default=dict)


acm_stores = AccountRegionBundle("acm", AcmDummyStore)
