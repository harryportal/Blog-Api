from flask import url_for
from flask import current_app

class Pagination:
    def __init__(self, query, request, resource_url, schema):
        self.request = request
        self.resource_url = resource_url
        self.schema = schema
        self.page_size = current_app.config['PAGINATION_SIZE_PER_PAGE']
        self.query = query

    def paginate_query(self):
        page = self.request.args.get('page', 1, type=int) # get the current page
        paginated_objects = self.query.paginate(page=page, per_page=self.page_size, error_out=False)
        objects = paginated_objects.items
        if paginated_objects.has_prev:
            prev_page_url = url_for(self.resource_url, page=page-1, _external=True)
        else:
            prev_page_url = None
        if paginated_objects.has_next:
            next_page_url = url_for(self.resource_url, page=page+1, _external=True)
        else:
            next_page_url = None

        posts = self.schema.dump(objects, many=True)
        return {'posts': posts, "next_page":next_page_url,
                "prev_page":prev_page_url,'count':len(posts)}


