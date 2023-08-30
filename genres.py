import openai
import csv
import time




def get_genres(book_descriptions: list):
    genres_all = []
    for description in book_descriptions:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user",
                 "content": "Write genres in a list based on this description. Description: A troubled young mother yearns for a shot at redemption in this heartbreaking yet hopeful story from #1 New York Times bestselling author Colleen Hoover. After serving five years in prison for a tragic mistake, Kenna Rowan returns to the town where it all went wrong, hoping to reunite with her four-year-old daughter. But the bridges Kenna burned are proving impossible to rebuild. Everyone in her daughter’s life is determined to shut Kenna out, no matter how hard she works to prove herself. The only person who hasn’t closed the door on her completely is Ledger Ward, a local bar owner and one of the few remaining links to Kenna’s daughter. But if anyone were to discover how Ledger is slowly becoming an important part of Kenna’s life, both would risk losing the trust of everyone important to them. The two form a connection despite the pressure surrounding them, but as their romance grows, so does the risk. Kenna must find a way to absolve the mistakes of her past in order to build a future out of hope and healing."},
                {"role": "system", "content": "Romance, Fiction ,New Adult, Drama"},
                {"role": "user",
                 "content": "Write genres in a list based on this description. Description: A work of literary suspense that deconstructs the story of a serial killer on death row, told primarily through the eyes of the women in his life.Ansel Packer is scheduled to die in twelve hours. He knows what he’s done, and now awaits execution, the same chilling fate he forced on those girls, years ago. But Ansel doesn’t want to die; he wants to be celebrated, understood. He hoped it wouldn’t end like this, not for him.Through a kaleidoscope of women—a mother, a sister, a homicide detective—we learn the story of Ansel’s life. We meet his mother, Lavender, a seventeen-year-old girl pushed to desperation; Hazel, twin sister to Ansel’s wife, inseparable since birth, forced to watch helplessly as her sister’s relationship threatens to devour them all; and finally, Saffy, the homicide detective hot on his trail, who has devoted herself to bringing bad men to justice but struggles to see her own life clearly. As the clock ticks down, these three women sift through the choices that culminate in tragedy, exploring the rippling fissures that such destruction inevitably leaves in its wake."},
                {"role": "system", "content": " Fiction, Thriller, Mystery, Crime, Suspense"},
                {"role": "user",
                 "content": "Write genres in a list based on this description. Description: An alternate cover edition of ISBN 9781982156121 can be found here.In this taut and explosive debut novel, one lapse in judgement lands a young mother in a government reform program where custody of her child hangs in the balance.Frida Liu is struggling. She doesn’t have a career worthy of her Chinese immigrant parents’ sacrifices. What’s worse is she can’t persuade her husband, Gust, to give up his wellness-obsessed younger mistress. Only with their angelic daughter Harriet does Frida finally feel she’s attained the perfection expected of her. Harriet may be all she has, but she’s just enough.Until Frida has a horrible day.The state has its eyes on mothers like Frida — ones who check their phones while their kids are on the playground; who let their children walk home alone; in other words, mothers who only have one lapse of judgement. Now, a host of government officials will determine if Frida is a candidate for a Big Brother-like institution that measures the success or failure of a mother’s devotion. Faced with the possibility of losing Harriet, Frida must prove that she can live up to the standards set for mothers — that she can learn to be good.This propulsive, witty page-turner explores the perils of “perfect” upper-middle-class parenting, the violence enacted upon women by the state and each other, and the boundless love a mother has for her daughter."},
                {"role": "system", "content": "Fiction, Dystopia, Science Fiction,Contemporary"},
                {"role": "user", "content": 'Write genres in a pyhton list based on this description' + description},
            ]
        )

        genres_all.append(completion.choices[0].message.content.split(","))
    #     reply = completion.choices[0].text.strip()
    #     print(reply)
    #     print(response)
    #     match = re.search(r'\[.*\]',reply)
    #     list_string = match.group()
    #     list_string = list_string[1:-1]  # Remove the square brackets
    #     genres = [element.strip() for element in list_string.split(",")]
    #     genres_all.append(genres)
    return genres_all


def genres_to_csv():
    k=22
    j=25
    while k<271 and j<271:
        books = []
        with open('books_goodreads.csv', encoding='UTF8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                book = {}
                book['title'] = row[0]
                book['author'] = row[1]
                book['description'] = row[2]
                book['rating'] = row[3]
                book['rating_count'] = row[4]
                books.append(book)
        time.sleep(60)
        book_descriptions = [book['description'] for book in books]
        genres = get_genres(book_descriptions[k:j])
        print(genres)
        for i in range(len(genres)):
            books[k:j][i]['genres'] = genres[i]
        print(books)
        with open('genres.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # writer.writerow(['Title','Author','Genres','Rating','Rating Count','Description'])
            for book in books[k:j]:
                entry = [book['title'], book['author'], book['genres'], book['rating'], book['rating_count'],
                         book['description']]
                writer.writerow(entry)
        k+=3
        j+=3
