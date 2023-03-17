from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from scripts import get_quotes_from_author, get_author_extract, get_similar_authors


def no_author(request):
    if request.method == "POST":
        author_name = request.POST["author_name"]
        return author_summary(request, author_name)
    return render(request, "author/index.html")


@csrf_protect
def author_summary(request, author_name):
    author_name = author_name.replace('_', ' ')
    author_quotes = get_quotes_from_author(author_name)
    suggested_authors = get_similar_authors(author_name)
    author_data = {
        "author_name": author_name,
        "found": False,
        "author_summary": None,
        "picture_link": None,
        "other_by_author": author_quotes,
        "suggested_authors": suggested_authors,
    }

    author_row = get_author_extract(author_name)
    if author_row is None:
        return render(request, "author/index.html", author_data)

    _, extract_html, thumbnail_url = author_row
    author_data.update(
        {
            "found": True,
            "author_summary": extract_html,
            "picture_link": thumbnail_url,
        }
    )
    return render(request, "author/index.html", author_data)
