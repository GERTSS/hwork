def mark_under_sanctions(self, request, queryset):
    updated = queryset.update(being_under_sanctions=True)


def mark_not_under_sanctions(self, request, queryset):
    updated = queryset.update(being_under_sanctions=False)


def mark_archived(self, request, queryset):
    updated = queryset.update(is_archived=True)


def mark_not_archived(self, request, queryset):
    updated = queryset.update(is_archived=False)