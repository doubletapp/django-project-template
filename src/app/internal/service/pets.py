from app.internal.domain.pets import Pet
from app.pkg.pagination import paginate

class PetService:
    def get_pets(limit=20, offset=0, min_age=None, max_age=None, fields=None):
        queryset = Pet.objects.all()
        if min_age:
            queryset = queryset.filter(age__gte=min_age)
        if max_age:
            queryset = queryset.filter(age__lte=max_age)
        if fields:
            queryset = queryset.values(*fields)
        
        return paginate(queryset, limit=limit, offset=offset)
        