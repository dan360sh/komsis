from .cart import (
    CartTemplate, CartAddView, CartUpdateView, CartDeleteView
)
from .order import (OrderView, OrderCreate, 
                    CalculateShippingView, AvailableView,)
from .favorites import (
    FavoritesView, AddFavoritesView, DeleteFavoritesView, RestoreFavoritesView,
    AddWaitingFavoritesView
)

from .compare import (
    CompareView, AddCompareView, DeleteCompareView, RestoreCompareView
)

from .payment import PaymentRedirectView