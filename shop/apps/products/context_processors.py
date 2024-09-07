from .models import ProductGroup



def build_group_tree(parent_group):
    """
    تابع بازگشتی برای ساخت درخت سلسله‌مراتبی از گروه‌ها.
    """
    children = ProductGroup.objects.filter(group_parent=parent_group, is_active=True)
    for child in children:
        print(f"Parent: {parent_group.group_title}, Child: {child.group_title}")
    return [
        {
            'group': child,
            'children': build_group_tree(child)
        }
        for child in children
    ]



def product_navigation_context(request):
    top_level_groups = ProductGroup.objects.filter(group_parent__isnull=True, is_active=True)
    group_tree = [
        {
            'group': group,
            'children': build_group_tree(group)
        }
        for group in top_level_groups
    ]
    return {'group_tree': group_tree}