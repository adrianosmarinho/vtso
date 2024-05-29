# Create your views here.
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from vtso.models import Company, Harbour, Person, Ship, Visit
from vtso.serializers import (
    CompanySerializer,
    HarbourCreateSerializer,
    HarbourDetailsSerializer,
    HarbourListSerializer,
    PersonSerializer,
    ShipSerializer,
    ShipVisitSerializer,
    VisitSerializer,
)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class CompanyList(generics.ListCreateAPIView):
    """
    View for the /vtso/companies/ endpoint.

    A GET request will list all the Companies in the system.

    A POST request will create a new Company.

    TODO: (bonus) change the view to disallow blank Company names
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class PersonList(generics.ListCreateAPIView):
    """
    View for the /vtso/persons/ endpoint.

    A GET request will list all the Persons in the system.

    A POST request will create a new Person.
    """

    queryset = Person.objects.select_related("company").all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]


class ShipList(generics.ListCreateAPIView):
    """
    View for /vtso/ships/ endpoint.

    A GET request will list all the Ships in the system, including their age.

    A POST request will create a new Ship.

    Here we leverage DRF filtering and search to implement
    the bonus requirement.

    """

    queryset = Ship.objects.select_related("company").all()
    serializer_class = ShipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["type"]
    search_fields = ["name", "type", "year_built"]


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="The ID of the ship to retrieve.",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={200: ShipSerializer},
    ),
    put=extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="The ID of the ship to update.",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        request=ShipSerializer,
        responses={200: ShipSerializer},
    ),
    patch=extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="The ID of the ship to partially update.",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        request=ShipSerializer,
        responses={200: ShipSerializer},
    ),
)
class ShipDetail(generics.RetrieveUpdateAPIView):
    """
    View for the /vtso/ships/<int:pk>/ endpoint.

    A GET request will retrieve the details of a given Ship, while
    a PUT or PATCH request will update a given Ship.

    """

    queryset = Ship.objects.select_related("company").all()
    serializer_class = ShipSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="The ID of the Ship to retrieve.",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: ShipSerializer,
            404: OpenApiResponse(description="Ship not found."),
        },
    ),
)
class ShipVisits(generics.ListAPIView):
    """
    View for /vtso/ships/<int:pk>/visits/ endpoint.

    A GET request will list all the Harbours a Ship has visited.
    """

    serializer_class = ShipVisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns all the Visits of the Ship specified by pk.

        Raises:
            NotFound: theres no Ship with the given pk in the database.

        Returns:
            QuerySet[Visit]:
        """
        ship_id = self.kwargs["pk"]
        try:
            ship = Ship.objects.get(pk=ship_id)
            return Visit.objects.filter(ship=ship)
        except Ship.DoesNotExist as e:
            raise NotFound("Ship not found") from e


@extend_schema_view(
    get=extend_schema(
        description="Retrieve a list of harbours",
        responses={200: HarbourListSerializer(many=True)},
    ),
    post=extend_schema(
        description="Create a new harbour",
        request=HarbourCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=HarbourCreateSerializer, description="Created harbour"
            ),
            400: OpenApiResponse(description="Validation error"),
        },
    ),
)
class HarbourList(generics.ListCreateAPIView):
    """
    View for the /vtso/harbours/ endpoint.

    A GET request will list all the Harbours in the system.

    A POST request will create a new Harbour.
    """

    queryset = Harbour.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Override of get_serializer_class so we can return the appropriate
        serializer according to the request method.
        This also allows us to simplify customization of the OpenApi schema.

        Returns:
            HarbourCreateSerializer if POST request, HarbourListSerializer if GET.
        """
        if self.request.method == "POST":
            return HarbourCreateSerializer
        return HarbourListSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="The ID of the Harbour to retrieve.",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: ShipSerializer,
            404: OpenApiResponse(description="Harbour not found."),
        },
    ),
)
class HarbourDetails(generics.RetrieveAPIView):
    """
    View for /vtso/harbours/id/details/ endpoint
    A GET request will retrieve de details of a given Harbour, including
    a list of Ships currently docked at it.
    TODO: add authentication
    """

    queryset = Harbour.objects.all()
    serializer_class = HarbourDetailsSerializer
    permission_classes = [AllowAny]


class VisitList(generics.ListCreateAPIView):
    """
    View for /vtso/visits endpoint
    TODO: add authentication
    """

    queryset = Visit.objects.select_related("harbour", "ship").all()
    serializer_class = VisitSerializer
    permission_classes = [AllowAny]
