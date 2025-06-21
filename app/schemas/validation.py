from voluptuous import Schema, All, Length, PREVENT_EXTRA, Any

user = Schema(
    {
        "id": int,
        "email": str,
        "first_name": str,
        "last_name": str,
        "avatar": Any(str, None)
    },
    extra=PREVENT_EXTRA,
    required=True,
)

response_list_users = Schema(
    {
        "page": int,
        "per_page": int,
        "total": int,
        "total_pages": int,
        "data": All([user], Length(min=7)),
        "support": {
            "url": str,
            "text": str
        }
    })