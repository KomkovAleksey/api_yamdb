from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Category, Genre, Title, TitleGenre, Review, Comment
from users.models import CustomUser


class Command(BaseCommand):
    """
    The command to import data from csv files to database:
    python manage.py import_from_csv.

    If you need to update the database:
    1) Remove db.sqlite3
    2) Make migrations (python manage.py migrate --run-syncdb).

    A new empty database will appear.
    """
    help = "Loading data from csv files."

    def handle(self, *args, **options):

        for row in DictReader(
                open('./static/data/category.csv', encoding='utf-8')):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        for row in DictReader(
                open('./static/data/genre.csv', encoding='utf-8')):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()

        for row in DictReader(
                open('./static/data/titles.csv', encoding='utf-8')):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
            title.save()

        for row in DictReader(
                open('./static/data/genre_title.csv', encoding='utf-8')):
            genre_title = TitleGenre(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
            genre_title.save()

        for row in DictReader(
                open('./static/data/users.csv', encoding='utf-8')):
            user = CustomUser(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            user.save()

        for row in DictReader(
                open('./static/data/review.csv', encoding='utf-8')):
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

        for row in DictReader(
                open('./static/data/comments.csv', encoding='utf-8')):
            comments = Comment(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            comments.save()
