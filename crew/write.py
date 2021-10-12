from .models import *



def posts():
    response = []
    posts = Post.objects.all()

    for p in posts:
        message = p.writeOnChain()

        response.append(
            {
                'hash': p.hash,
                'txId': p.txId
            }
        )

    print(response)
