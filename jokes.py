from bs4 import BeautifulSoup
import requests
import random

def mainJokes():
    url = 'https://www.fatherly.com/play/corny-jokes-to-tell-kids-you-love-and-adults-you-hate'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    # This is the bug (containers is empty [] - will need to scrape again)
    try:
        containers = soup.find_all(class_='article__content article__content--dropcap')
    except UnboundLocalError:
        print('Containers is empty')
    else:
        all_paragraph_tags = []
        # Loops through every section in the div class above and finds all the paragraph tags
        for section in containers:
            paragraphs = section.find_all('p')
        
        for i in range(len(paragraphs)):
            joke = paragraphs[i].get_text()
            all_paragraph_tags.append(joke)
        del all_paragraph_tags[0]
        del all_paragraph_tags[-2:]
        # print(all_paragraph_tags)
        num = 79
        i = 0
        list_of_jokes = []
        # Loop that gets all the jokes into a list, ready to be processed
        for _ in range(len(all_paragraph_tags)):
            try:
                if i == 134:
                    full_text = f'{all_paragraph_tags[134]}'
                    list_of_jokes.append(full_text)
                    num -= 1
                    i += 1
                else:
                    full_text = f'{all_paragraph_tags[i]}' + f' {all_paragraph_tags[i+1]}'
                    num -= 1
                    i += 2
                    list_of_jokes.append(full_text)
            except IndexError:
                break
            else:
                continue
        list_of_jokes.reverse()
        
        # Replaces the number in front of the joke with blank space
        final_joke_list = []
        for i in range(len(list_of_jokes)):
            final_joke = list_of_jokes[i].replace(f'{i + 1}.', '').replace('"', '')
            final_joke_list.append(final_joke)
        
        # Deletes last 6 jokes because of bug that would'nt let me delete #s attached
        del final_joke_list[-6:]

        random_joke = random.choice(final_joke_list)
        return random_joke
        


    


        
    