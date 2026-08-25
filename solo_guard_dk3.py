from dronekit import connect, VehicleMode, LocationGlobalRelative
from flask import Flask, render_template_string
from flask_socketio import SocketIO
import threading, time, random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

KEYWORDS = ['mariposa', 'paraguas', 'cangrejo', 'telepata', 'murciélago']
IMG_SRC = "data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAIcAhwDASIAAhEBAxEB/8QAHAABAAEFAQEAAAAAAAAAAAAAAAYCAwQFBwEI/8QAThAAAQMDAgIHBQIKBggGAwEAAQACAwQFEQYSITEHEyJBUWFxFDKBkaEj0RUzQlJigpKxweEIJENTcqIWF2ODk9Lw8TRWo7LD0yVFhJT/xAAaAQEBAQEBAQEAAAAAAAAAAAAAAQIDBAUG/8QAKhEBAQEAAQMCBQIHAAAAAAAAAAERAgMhMQQSBUFRYXETwSIjMkKBobH/2gAMAwEAAhEDEQA/APjJERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQERZNDQVtfJ1dFST1DsgYjYXYJ5ZxyQYyKcWjox1BVRNqbg6mtdJ1nVvlnkGGk8snO0Z83BZ5sXR3YJo2Xu/TXWdkjo54aEb2tx3gtIaR6SIOcIpZftR2KS2SW2xaYpqRsgLX1NQetmxuBBZ+bwGDku5nBCiaAiIgIiICIiAiIgIiuU0MtTOyCCN0ksh2sY0ZLj4BBbRZc9tuMAcZqCqjDfeLonAD6LEQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQERbq16V1FcmF9Haal7RjtObtH1xlBpUXQaHom1JP1bppaKBjhl2ZC5zfgB/Fbyi6IDT1DJqqubXMYcmna0xh/kX8cD4K4ORL1oLnBrQSTyAXY79b9E2RscFboC5tqJztiJrR1bj5EEk/JWqnWWkNJR09JatKQz3SJrjUGRmz2abHBoc7c5xaeBGG8RwPhFxzyzaS1Hdwx9DaKl8T3bRK5m2MHzceAUppui2qpqcVd/u1JbqdhHXEn8XuOG9p2GnPkSsK99KmsLkZGx1kNvikiET46WIDI7yHOy5pPiCFD7hXVtxqTVXCsqKycgAyzymR5A5DJOURO6Y9GVl6t9Q6vvc8crmSMjbhrm/nAuw304O8VhXbpEuEkIpbJRU1mpg1rQIhukO08DuIwDy5AKEogzbpdbldKiSe419TVSSO3vdLIXZPisJEQEREBERAREQEREBERAVUb3xva+NzmPachzTggqlEG9drDU74mxSXuskYzgA9+7h4cVmDWcs7ohdLFZbhEzm11N1Zd+swg5UWRBKay+6YrJRv0fHRxZ4ilrXhw9NwK9cNA1c7GRyX22MPvPeyOoA+ALSoqiCUVdo0iXiOh1TJI5xw181G9jR688KtmjHVMwp7df7PWzkdmOOowXemVFEQSabQupIy9raSKZzPebFOxzh8MrBm0tqOFpdLZK9jRzJgdhYNBcbhby80FdVUheMP6mVzNw8Dg8VtaDWWpaGl9mprrK2POeLGucD/iIz9UGndR1bZOrNLMH/m7DlVNoK5zdzaKpcD3iJx/gpbSdJupIqQU85p6rAIMkocXnPnuxnzwp3oSt6Q7/AEUMtv1JWU9pkDhL1EzDLGG8xggE+mUXHEZYpYXFssT43DmHNIKoX0y3QVI6Prap5ubpcSGoqPtDJkcDk+q8/wBBLWBwtVG7zMDfuVxMfM6L6Mrujy21Eex9opgP0WbT9Fp63optUjNsdJLAfzmSEn65TBwtF1m4dEWA32Stniwe11rN+flhR+v6Mr/AXGCSmnYBkdotcfgR/FQQZFu6vSeoqSIyT2moa0d4Ad+7K1FRBPTv2TwyRO57XtLT9UFtERAREQEREBERAREQEREBERAREQEREBERARFn2qz3S6SBlvoKioJdtyxh2g+Z5D4oMBF0jT/RJeaza+51EVGwjJYwb3g+B7vqV0vTPRjYLaWubb/a5Rn7SoG8/Ll9FcX21wKyabvd5eBb7dPK0nHWbcMHqTwXQtN9DtTNslvNaIwcEwwDJ8wXH+C7pTWlkEYbsZExowAcNACyoYIet6pkjHPIzsZ2j9Fci4hWnujyxWtrTTW6HrGjHWyDe8/EqUQ2iOMeHdwWNPq3SlFPLBUX6hjlh99j52sII7sOI4rRP6X9CMdI326XLAcZheQ4+RaCglDqJsY4BUGE5xj1PcFzx3TxYd7m/geua0Z2uaGuz83NUa1F0v3yudIyzR01LSPb2Hvg+2HjntFoPomot9Jd7qqnpPo6O0wvq5aF0ccMbBuLptwfgDvOQBhQTUNNVXHUdwdUU8tPdZqqWWpikAaGvJLnDHdxz+5YdSXGV9a6WUzveXmTed27PPPipH0cyxvrq98o3SMoKja53F3GJ3esiDoiIgiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiDdWW1Mq6CSpeJC/eI4WNAPWvJGBx90c8n04Le09/vVrtctTZr3FZ2scIDQQSFsrstAc/GMcc8TnPBaanrGxaSEAwJjVHb44wMn07lapXPqAHzdp2cZx3cEa+Tumi+kuot8dLTavttMy2VEcbKeqoXte6F+0DD4gcjOOOBwdu55K6my8aTNXNSfhqibUQnEjHTsBafmvjuiiMmoaeFoOHVDG/MgLXXgk3esJGCah/D9YpLSvtaS46dJw27UR9J2ferEtZYzyulL/AMdv3r4lRXU19lzz2lw4XWl/4zfvWFL+C3Z//KURz4zM+9fIKJpr6wnitGM/hSiH++b961Nfb7DNxluFsee7fI0/vXzKiaa7lcdJaRmDx11ra5/NzJ2tPw48FH67QenHR7Ka7wROB972pjvoSuWommpvW6DiZL/Vr/QGPH5cjd30Kil6oJLXdKi3yyRSPgdtc6N4c0n1BIWGiiCIiAiIgIiICIiAiIgIiICIiAiIgybZVCiuEFWYIpxE8O6uRuWu8iF1yi6YbNStjDdMyuGO2GztZg+Rwc/JcaRF116t6c7o2tLrZZKOKkxhsVQ4vd6lzNq0FR0v65krH1Edyiia48IfZ2Pjb5YeDn4qAIhtSeu6QNZ1lcax2oq6CYjH9Vf1AA8hHgLQ1tfXV1Q6orayoqZne9JLKXuPxKxkRBERBepKaaqnEMLC5x4nwA8T5Lb1kMVE5lKHmTqmYfI0ZY92SctPhxHNe6Np5q2pqaKmMQnfFubvOC/bzaP3/BZU9DcYnmOSneMeHFFytTNLF7MWbsuyeCotddU0NWJ6R+JC0sIxnc1wwW478g4W9oxNC8F8Dv1mqQ0F1pY9omoaV+05G+BhwfiFVyoBNTxwVLo6qCencDxjcMFvz4qhtPA9x21IaO4ELsbtVUdWB7dQ0VVj++po3/vCvU1fo+omZ7XpmzvbntYpQz6twmJjjdJZ6+rkEVJCamR3ushBe53oArFdQ1lDJ1dZSzQOyRiRhHEHBHqDwK+x+jZmgoIZBY7bBapahobMaeV7C8eBO7JHlyUgveg7Dd6D2WSgppqYtw2MsGGjy8PgmGPg9F9Ha26AKN4fPYqiSilyT1cmXxHPd4tA4+K41qvQOqNNue6utsj6dpP9YhG+PGcZJHL44URFkQgg4PAogIiILtLTz1VRHT00T5ppHbWMYMlx8AFM4OizV0lIKmWnpKZu3c4T1DWlg8/BSHoA0xVyVcmrKimIooC6nppXAjdMW5dt7jhp4/4guxuAeC1zQ4HmCM5QcHZ0OaycA7ZbwCMjNSPuVT+hrWTHbXtoGu8HT4P1C7zucDkk5SSeQuLnve5x5lxJPzQfP/8Aqj1fvewNtxcw7XAVY7JwDg/Ag/FRzVWlL5pmVrbrSdWx5wyVh3McfAFfTpkAyQACTknHMrGv2mZtbaXu9go2b611G+opGhoJfLEWvDQTy3AEZ80HyeirnilgmfDNG6OWNxa9jhgtI4EEeKoQEREBFJ9J6E1PqZ7DbrbIIHHjUSjZGOODxPP0GV2XRfQLQ0xjqL/UmulGCYW5ZED597h8kHArNZ7peKj2e10FRVyeEbCcd/NSDUHR3qWw2qO63GmZ7C9waJqeRswBPc4NOWn/ABAeC+sLbZ7Hp2ibBBBT0sDBwYxoA4fv+Kjmq9dW+kjfFT9W4gc8Akq4uPlKGgklIMFJVz457YiR9AttbNO6gmcBT2CXY78qeAho+LsKf3bV0tTVPex2Mn8jh+5auW91cnERynPkUXEQuunb1TXCWA0LperOOsgaTGeGeycAYVEFHcKRu2WiIAOeLwCpNNWV8v8AYv8AiQsOWnrZuYaPVyL7a0ERqobkysYRE+OQSMOQS0g5B81k3K1MuDay5Wprw2LMssD37ntb3uzjj4lZ4slTO8AyNHoCVILnZ49J6ArLo+SQ1tx/qNOXNyNrhmXh3djhnj7yiWX5uXIiIyIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiIM+wXOaz3mluUHF8EgdtzjcO9vxGR8V2OeG33qjZdLTIyaGQAkNPajPe1w7iFw1ZltuNVQOd1Ejgx/vsycO/mpW+nykv8AF4dUfb3tPFjh8FbNH4tWm07frPNGwVd4loJXPDdsscjmAfnFzc8Pgpe2C2vqIoaTW2n6x8rg1jG1j25J5DtsGPivLy6/Pjf6K/S9D4d6PrcdnqOEv32fs0rqFvHLG/EKn2BmfxbflhT+16IvFTVFtVKyKJpwS3a/d6EcMeanVk0ZbqAiXqGmQf2jxud8DyHwwu/S6l5zbLPy+b8R9Hw9Jz9s5zl+PDk+nNKajqZGy0L5KGM8eslJAPo3mf3Lsuj6K+W2BkVTeZql2OXVBo+A4n6raR08VNGXkNjaBkuPNc/6RtRV9SKizWxzqWBnZqHtd9rJn8k491vlz8ccl2fLxOI+kawm7S2uSuhqXRHa+Vnu7u9oPfjvI4fJbow2e7x7oXsyRzC+UamgfDJuj3ROHIt5La2LWF5sr2gyvdGD48EMdX1n0NadvIfIaBsEp4ielxG7nkkjkc+YXIdU9BF6o5Xvs1bFUxdoiKoHVvA7hniHH5LrelulOOpY2OqIDu/Kklx1faX0RkLmEkcAoj5Au2htXWsMNbp+uZv93ZH1n/typT0NdDup+kPUvsRpai12ymIdX1s8RaImn8loONzzg4HxK7K3UjqqubHC4tY54GB4ZXROi/WVJatR1Om7i7qhXGLqJ3HAEwb7h8A4uOD4+qYYudIdjtOldM6d03ZKcU9BRtlDGjm7gzLnHvcTxJ81zW6+1PkYyFrzFjtbTgZz3rqPTZIXV1tj/NikPzcPuXI73VVrKiOnpmSBrgC57GE8yRjPcpUbB0EOMdU31I/isRkNU2R4Y8Mjyccc8M+Cr9hgZ74dM7vdI4nP8FiyGia9zfY5wWnGWQu+hCC+Wua8bmSvIPvOOAPPCmHRNOYteW/J99srP/Td9y59HPVR1rWxNqX07nAHrYzwz9yl+gqltLrG1TSPa1gnw4nuBa4FIMX+l30Ox3KjOv8ASlCTXtcG3WlhaPtmngJgPzgcAgZzkHxz8w23RuqbjJspLFXOOM9uPqx83YC+zdfdLFkqdKtpbFUOqpbg8NLi0gRxNfxd6ktw3yyfDPOtVXWSirRseQ0jc3w5n+GFcazXMNL9CGoLiGS3Wrp7cxwB6tv2knPkQMAcPMrr+keh7Sdj2zSUYrJm5+1qyHn9n3R64Wvs+t44ou04bgsS/wDSNI2MtjeR4YKJjptbcLTaYj2oxtGFBdT9J0FK1zKZwJ8lye76lud0ldskdtJ554LbaCGnm1DmaitpqZHuzHVPc57I/J0fh+lxPl3qrIxb1q693qRwbI6OM95K1jKOWY7pnOk8d33Ls8+kLHUwNmgoaYxvG5kkIwHDxBbzWun0fQilmijmq6aY46qVgZIG+IcxwGR5hwI8Cs8tkdujxnLlJezmDaXbgBqrbRvPJh+Sr1c66aXqOrqqCevhd7tRGXBhPhgjgVpYdaWnbuqaWqbIPyGMafqT/BeO9brfLp/7j9H0/Q/DOM/m+pkv248r+zc+y7feLWj9IgLx7aZgy+oiA8jn9y1FVrix+z5prZcH1H+0ljaz5BpP1WCzXUGxwl09TTkjDS+plAHnhpGVZy9Ry/tk/wAs9WfBunxvt63Llftxz/tTuxQ2z8H1l7rK2OC3UG0TTvBaC8+7GzIy9557W5IHE4HFc56SNWv1VdYjDG6C20bDFRwOxloPFznY/KceJ8OA7lrL/qO6XqnpaSrlYyjow72emibsjjLjlzsDm48MuOScDjwC1C9XHc7vznW58eXO+3wIiKuIiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiLcaX0xfdTVfs1lts9W4Eb3Nb2GDPNzuQCDTrJt1BXXGoFNb6Ooq5iM9XDGXux44C79ob+j7C1sdTqqsfM88TS0x2sHkX8z8MLtGnNM2XT1IKa026no4+Z6tgBJ8SeZVxcfOWi+ge/3IxVOoKiO1UxwTE3D5iM8vBvDzPou06R6LdIaa6uaktjJqlg4VFT9o/Oc5GeAPoAppLIxnADisc1GDgcT5dyY3xuLgiZG3stGVZqJmwjLzvcTta1ozknkAO8+Sx66vhpoHyveMNaXOJIHZAySSeAAHEk4A5lfNPSx0sV96qam12GoMFvIdFJOzIdM08w0ni1p5HkXDngHahebf8AS50xVjK2ez6aqGB0fYfWxu3dWeIIjI4F36Y5fk/nHjdmvl0tFU6ooqt7HPOZGk5D+OeI71rUUc3XdMantuoWR0tSG01ydkdXjsSEfmnuPks2st21zhtz5YXILRAai4wxgkDdkkHiAF1a6aloLSaOhrpJpamRu6SUnLWtx395OcjPgPimty/VjOtswdupDskHHaTwP3KxHcK3rTBO57S04c09xUho6qlqYmTwSNexwyCFh36Fk1RFM1o34w4jvAT8Ljc6Mc6W5U/EniT9CtndsVuortFu4tlw3jywFh9H8YN6p2YJ78fED+KjjdQbNe3Iud2HVbxjyyrPDN8uuP1TU6jtdtdXPe+sooDTVUjucj2vcQ71LS3J8crQ3Opey4BkF3jpp9g+wmA2PHHjk96zbBTtdTSyNZnfMXAj/C1bF1Hu96NpPLi0FRlFbpcL5BTYNG1hHOeHttI8hxx6lZNDROqKGGomra2R8kbXkicgDIzwAUmobTPWUjKmkfTGF4OxxqGMz3ciQrzbBXd8tEfL2yL/AJkEBr62rtt3ZSipllhdtJbKdxwTjmpBR1UVDdqSqqQTBBM2SYAcdgOXD5ZWf7M0lwbhxa4tJbgjIODx9R3KzXUIfSTtLecbh9Cg5zeKrrY5qx7WxmR5e1jeAaM+6PIDAHotzr6QyUVuqQeMtO1xI/wt/moHqe4dWxsTXjIGOCmd8kNToSwVR5mFrD64cP4BVtAaiskjedristlsqXNbLWghzhkRHuH6Xn5Lynp2/hOOQt4Ndn5LeTztc/jxcTgDmSVI1jDpKAEjs/RbG41Nu0/Zjda1zZGiXqWQRvHWPft3Yx3DGMuPLI58lqL9qm2WFtTRCnNfdm5jDBIOopncOLi38Y4ceyCGg8y7kNNrKoo7uK2spqWGjjq4o6yKPJPVvDe0xvgDl3A8g0BLWbfo2lg6Zb3bbqxxoaNtq3HfSRMwS3xLs5LvM/QcF3rRmo7DrG3sqrVO0vLcyU7yOsjPfkd4818arY6dvVxsF1iuVrqHQVEfIjkR4FGZysfaNRasj3QR5qKX/o20xeWu9rtELJTkiSEdW7J78jmfVYPRX0wWvUUEVvvcjKO5hvaceDH478/X+HeupPia9oewhzTxyDkHzVyOnvtj521H0DODHS2K6nIaNsVUM5Pf2m8vkuc6j6O9W2N7vabTLNEHbRLT/aNPy4j4hfZMkQ8OIWNLTNP5JKY5vhV7HseWPaWuBwQRggqlfZGoNF2K8DdXWmlncM7XOjGR6Fc11F0JWuUOfaqioo3hpAY472Z8STxTDHAUU01R0aamsgfKKX22mZxMsAyQMZJLeYChjmua4tcC1wOCCOIUR4iIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICKqNjpJGsYMuccAL6q/o+0P9HG0afpq/VbJ7pfwz+si4wGSna48xGxvZI83cfRByzoV6JKrVj4bzeGyQ2gOyyJoPWVOPDwb58z3eK+odPWW2Wa2xUVsooqSnjGGxsZtweXHvz68VpOlLpf6LaegadMQUkcsB+zhpGAun7tjmN7Ebf0id3gPGqt1/pOkqn0kNZIycYJYaKVjsEcOBZnlhVqJXI9jOyCtdVVYAOCCo8dV2+pZ10dU1sR4Bz43sH1Cxpb7bpBu/ClHjHdKMqq2z6gyPIB8yTyWvut4pqGlllfNHFDEwySSyP2tY0cNzj3DPDxJ4AEkBRrVWsrbaraah9Q2ODBPWObwfjgQ0flnyB9SBkjgPSTr6s1XK2jp2SUdoiduZAXZfO/8AvZSOBd4Adlo4DmSYluNv0rdKFVqZklntHWU1pJHXSOG2WrIORu/NjB4hnjxdk4xzREUZEREGytD/AGb7cN3Pc7a0Y7hzWy1cYrpqapkoKmSpoI9sVPK9mwljWjmDyOcrCg3MLIwcNZhgAPvOPE8fAKSU9qpae0C83ypfTW7OyCOJmZqt3gwcmt79zuAHc4840wbBPcYZoqS1RSTkuwImgu3Hwz9wXRaOFtRb2yGanfMPxscUzZHRH81+0nB8lyq6akqJmmmtcQtdHsMZjhed8rTn8Y/m7hgEDDeHuhdA6E6fGl7rVSN7LqlrGeZDeP7wjXG98TbQEfV3d0zhwjjJ9Mcf4LjNxkmdcaqvYDwmLnO9Scfx+S7ro+n3mtBeGdZH1e4j3d3DP+Zcc1dYK6z3h1pq+rE293FkrXsLQSC/LScDDSePEd+FpLNrtfRlVCt0dSVBO5xLg4+fD+GFJMYPBxXzponW15sVykpbXLHLbnnLoKhhIcRw38CC1x8j4DjgLozOkqdzQZLPT579k7gPqCoxU/dTwn+yi/ZCdVGBjqo8eTAFAT0jv7rMz/8A0n/lVJ6R5+60Q/Gc/cr3E+EYaNrNrG+QVMuGwSFxAaGOJJPADHFc/f0i1pHYtlI0/pPefuUT6QdZajr7SYo6ttLTOdtmjp2bS5vgXHLseWcFQRS/tqHXeoiLS0xHL2u4Fo9F0mzu9s6KaIczTVDo/TtDH0cuYz1JrjDcXkHa0Qz920gcPgRy9MeC7PY7DPaujwU9VDPFUVLG1xilbtLWPLurIHg5rQc+OeWMI3EestrbVVAjkljha7smV+drAeGTgE4+ChldXvmq6mSi6qvoInbd8YIIbnAcQQCM/pALqmmWGGsZI0AlvEZ8RxC4DdG19p1BVxOMtJWU872O2OLXMdkgjIUjXO43Mtvtte1zqfEcp4lp4EHHeOY/crLPabfNTMcJDGzsl3POeeD4cfqrFHdKerkiiuDW0zwQBVwtxt7suaP3twefBy292pqiKKejqWhtTDh2QeDh3Oae8EJWETuNP7LXSwD3Wu7PaB7J4jiPIhY62l5YJaWmrGjiQY5MMwARxGT3kgn9latVl60lrg5pIIOQR3LqPRX0wXfS8kdBdXSXC1lwGHu7cI7y0/w+/K5aiD7v05fLRqO3NrrVVx1MLuJ2kbmE9xHcfoVnPhLOOOyDzHcviPROr7zpK4tqrXUvazcDJFnsvHf/ANfPK+nOjrpYsepqZsc80dHWZ2mKU43HHd8vTzHJWLHQC1u3kFjSwsdywfFU/hO0yABlzp3Odyax28+mG5ytRddW6Ztk8tPV3AsnjbufE9nUuAx/tS0Iq5X00QbnHH9ELmPSHoWx3pj5Xsio6zjidmATxPvAcD+9b8dMGiZ3ODKuKIeNVK9gP/DjeoLq7pOcL5WOoaG1Xeyysj6osfJ9i8MAdtkLGEZIJ2ub6eKaOT3zSt3tdW6E00lRHk7ZImlwIHecclonAtJDgQRzBXXqG7VGooSbQbfDUnOaN1S90rfQFo3D0ytJeNHV9dbzJI2Ft1FQ58jzuHWMLWgNxjA2lrj4nd5ImOdotrd9PXe1vcKuikDASBKwbmOA7wfBapRBERAREQEREBERAREQEREBERAREQEREBERARFNtI9HlzuzWVdycbbQnjl7ftZB+i3+J+qCG08E1TMyCnifLK84axjSST5ALoGm+iy51HV1F+mFtgPHqvemI9OTfiur6M0lSW+Eiw22OnbGz7avncA4DkS6R3BoPgMBYesNc6S0i2WGnMeoLyz8l25tMx3Hnyc/4lo8NwVXFVj0VZ7bSOrqOmp7fRwNImrqojgOZy8/uAyfBbS2RW+4WOU6Uu9JSbm/+OFKJZMbsHbGSBGeIwXZPEcGrjsWudbahvYl3yXGprYpaOmo4ozsYx4w9kcbMAZBxwWgvtbWUu2gED7fLTvc2VkW5na4Ag5OSQR3qavd0q5aRsWkrddbrVTT32spqR0rWPe2IRyP7DJS0ElwbI5pwSQe8Li88tTPM+pmklkleS50jiSSfElZ9rqa72iWSJzZHPbiTru0Hce/K3VE+inuNsbHDsquvc2pYXB0D2g8gBnOR681Eze6MR1tZG3bHVzsb4NkIC2FHqnUtHCYaW/3OGNwwWsqngY+a1Bxk4GAvFUXqmpqalwdU1EszhnBkeXHj6qyiICIiAr1E3dUtyMgdrGOeO5WVs7LFkSTEchwP/XnhCNnYKIVl5ZC8bo4T2/A97vnyVXSVXy1F+9icXBlEzqww4w1xwXYx3ch8FvdDQR0FvqLtUAbImOlcS0uBDeOCB3F21vxXPqqZ9TUy1EmN8ry92OWSclRq+Ftd26KI3Do1pstxuqZXDhz4gfwXCV9J6OhbH0b2MBgYPZA92BjJJJVXh5SHQjYGOklqSGQNkY6V7uTWB7ST8gV8/arqKakM4pWuDq9xezecubTl2W583ntf4QPFdqtMkNdbrpZX431UDmMbv27ycYbnuzxGfMLglfT3Cu1NVMuMMkFU2U9dE9u0xkfk47gBgDyATO7d5ycbJO69p2nLIzM4dp/j4LfB2BhW4YBExrQAMBVo4qg8pvVIHgmMIKw5eVMTainfC/3XjBVOcclej4qyiHUkptlyfDUxmSB32c8f57PLz7wfEBfQmgdQPvGi/8AR25S+1Vdppi2lqj/AG9E45iPq0hzfLOO5cU1XQxPgFU2RjJm8C0uALx5eannRmK3T2jaqqvLepNT9lQQvbiXqyQ5xxzDSQMDxyeSmOnHlksTCxRtFWGu55wuFdLNHU0XSFdmVQ7cs3Xg+LXgOB+q7dYajry2YcHcyuZf0ibfNT60p7g+UPZX0bJGDPFu0lhB/Zz8VJ5Xn4c0U6gqRctNUdW47paP7CXjk7Dw4n5H4lQVSTQ1Qw1FTbZXYZVRkNyeAcPLx+5Vz4+VBgDqevoHloc1pliLiQAW8eGO8jcB/iUeUpndLS1dNWN4SxP6t58wf+yj1yjiiuE7KcPEIeer3+9tzwz54wpCsdERVBVRvfG8Pje5jhyLTgheYK8QZ7r1eHU7ac3WuMLDlsZqHbR6DKwpZJJXmSV7nvPNzjklUogqYwvOBgeZW8paWoo7DVySTxthmcwhjXZLnNzt4cuTitZbmtkf1ZxuLhz/AHLcaomqq6qZJOWMiYwNaGNDQ39X5BFYNoxLc2RcMuf2cnAz69y69eukumjubaausFNLTtootzqU4InDG78gkYG7PBhA7wO5cVpowZW5kc07hjaOPqtvFRT3SWJ0tRunc9rCSAMZIHIcznxRXTrRqjTd6k6ilrpLfO4Y6mrbujfwzgPAz82481j6j0bQ1URqKi2dSH+7V0hBjccc8ty0+nBct1WYDqa5ey07aeFtS9rIm8mgHGPosyxay1HZpQ+juc2Mgua924PAGA0nmW47s4V1NZd60XW026Wgf7XEPycYePh3/BRiaGaB5ZNE+NwOCHDHFdTsnSTZK1gi1LaOonJA9qoQGA+Jczl8AFvnWix6ponSWetpLtGBxif9nOzjjkf4FFyXw4UinF90M6Cd7aZ8kEg/sJ2kEcfHw+CitxtVfQH+s0z2t7nYyPmomMFEREEREBERAREQEREBERARFvdM6Tv2oX5ttA90IOHVD+zE3x7R5+gyUGiUk0vom/ag2zU9KYKMnjUz9lndy73c+5dY0R0VWujljfUQvvdeOONpEDD5N/Kx4nh5KV6rv2ldIQB1/uDaytaB1dto3AkDuBI4AenDzCuLiOaJ6PLdbXtNDRuudeztOqpm4bH5gHg0DxK3mo77pXSFPJPd66K5XIN3R0cbztLvA44nj/hH6S5Rrfpdvt8glt1rjjtFsccNihGHkeZ8fmfNc5lkkmldLLI6SRxy5zjkk+JKGp9q/pa1Tfg+nhnjt9FgtjhgYGiMZPu/mnBwSOJ7yVz8kkkk5J714qo2OkkaxjS5zjgAd5URIrHDHLpuoOCJI58g+RaPuVq6sc2ohgyCxzQO8cPDnxW0ofY7Zp6S21L9tdM8Th2csczGNoP5wIOfVa68+/SP8WjipjXyYFI8tqhEA1o3Y90E/VbS4f1Wpt88bnNIkBLt3HmtUzDLmRyAkKyb7VRSdRHG8OMeS4jlxVR1a5/0c75ZbdWXHUV/s9op4SXMEkzpJCzPDstbxOPAqK2vS3Rk6VjLlr64xguw4xWpu0eeXS5x8Fcb0czVcFPW1+obdQsmhbJipqhNKMjPuR7ncuOCAr7NFaLpG/1u/XS4P/NpadkDP25CXf5EMXtXWjoOsdrm/AWpdRaoupYOoaaUU9KHE83uID+AzwbzOOK0fR1Do641lZR3yx3GtnliDbdDb5HNe6bcPfJJw3bnjhbl9DoyCB0dNYcu4fbVNW+WQce7G1n+UqqK6UFGwtpKSniHfhoVxcLf0WMrrxHRVAqrduaXEAtkMYwSC7w7h3ZytrUdAVU7jR6hhI/2sBz9CrFFraopnYDwBnOAMBSW29JfVgdac/FMRDbn0E6pp9vsVdb6wHn2jHj5hbaPoXvdPbRDDeLW6V+C8OEjccOWdpB5qZxdKFE5uHLIi6RLdJxL2pioRq3Quo6DQj7db6M1tXNNHG9tI8uxEMudkYGQX7OH6K5t/q81x/5YuX/CX0bBre1SAZkas+n1Xa3+7M0fFMS93zPTdGuup5mRN0zXsLzjc9m1o8yTyC+nbfpp/wCCKCglLWtp6eONzWcAXBoBWXBqG2OGDMz5rKh1DbmnLJWn4pizs1FXoOmkZvY50cg/KbzWhu+mY3ua28QU1zbGMMdUR/aNHcA8dofAqbVWqKRsbi145KE6j1G2YuLXA/FVO7R1+ndHAnNqqI3/AKFfLj5bgtTNZdMNPZop/jUyn/5Farrlue47ufNYPt7dxa92AeZxk/BTFZT7VYG+7Sy/Gom/+xUfgyyHlS/+rMf/AJViS1bus3N2Fu3LRjhj71b9taYxJwa4OwccimGtpHbLF30ERHm+b/7VkRWrTbvfs8LiP9pIB9XFag1v2Ti9sbeGWlveUiuGMHn8UEooLPRCQOtdvoaKQ8pY4B1g/WPFSO1aFjqH+01kktTKebpHElRSxXcRPaS4Lolg1ZSxBoc9o9VRch0iymw6IOaRyIUI6aOji56ogt1VZ276+mLopGSSBkZiOCMZ/KB3Z8QR4LrTdZWcRgOdGPFWTrOxtPvxnCmHl8wDoT18Tj2GkH/9TVmWroW19T3GnmENFDskBMntIdtHecDmvoWs17ZIwcPZ81pK3pPtsRxGGnCYmI6/oVt1W+V1XdK5wlILmwxMZgjhkE55q3X/ANH6w1VQySG6XOBoGHBxY8uOeecDHyWyqeleBuRHFla2fpaqj+KgTFbOn6B9ExMb1sVZK5vMuqSMn0Cs6w6LtNss7I7ParbFOx4Ly84e9uDkAk4zyPHGcc1oqzpQvMzSGN2tIUer9XXerJ3yuwe7cgw9baeqqCztt1B1FW0v6za+ldFNAeHJ47LgcYIJI5EeKh9ll1JaK0TstT6uOI75aeem6+B7eRD28RjjjPDyOVK2Xuracl72+hKy6PUlTBKJoZ3xS/3kbix37TcFMFim6S9EuAZdOh/T7nDg91NKYvkC0n6q+dT9B9fk1fR9d6Bx76Sr3j6vH7lsX6plrBtr201waeYrKeOoP7T2lw+DlhSx6SrB/WdM0kbiffpJXwn5O6xvyAUTEL1hLpB2paT/AELir4rb1TN7azHWdaXO3ePDG3vWv1IT2OPfxW01Rp+R93NVYmbqYNaWNkkYHtI5jAwCP+sLT3pte5jRU2+eF44k7SQfQorAtzd1YwcD6hTXRlOJ79RQhoxJXwNx+uFCqCVsFSJJWPAA8FvLbcbgHMNshlilEu9s3IsOMZHnxQnlp9U4/wBJroRyNZMR6bytaugXXS895slXdbfShs1C0OlbntSMx3DvIxk+q5+jIrtNPPTTNmp5pIZGkFr2OIIPqFaRBL7d0hX6GBtNXmK5wNBAbUNyRk5zu55UgpNTaauQLXuktsjs9iXtx4x4rmCJqy46bcdJUFVG6eOBpGPxtM7IyRkEj6qLXDSdTFudSzNmAPBruy7C1Npu9ytUvWW+slpzx4NOWnIxxB4HgpXateNklDL9QNmjO0GamAEjcDicE4cTw7wquyoZU0tTTO2zwvjP6QVldUhn01d4f6rc6cO2hxhquw4EnG0bveP+HK1t40Szc/q43wvHA7O0B6jmmJjnqLcXHTtxpCXNi65g45ZxPy5rVSRSRuLZI3NI5gjGFEUIiICIs21Wu4XSoEFBSyTv4Z2jg3zJ5AIMJbfTemr1qGo6m1UMkwB7UhG2NnmXHgF0rQnRVFI6OovLX1kvP2aLIjHL3nd/fy4ea6TdLnpPR9BDFeLnTUsQH2VFRgOd+y3058fVVcQrR/RPa6N8Ut0L7vXDB6hgxA08Dx73Y4+R8FLtTX/TekKaIXyqaXgARW6i2lwA8RyaOS5lrPpmuda00el6b8C0gP40HM8nqeQ+q5bUzzVM756iV80rzue97iXOPiSUHRtZ9MGoLxC+gs7W2O3E/i6YkSPH6T+a5xNLJNK6WaR8kjzlz3uyXHxJKoRRBERAUk0C63xV9VU19Manq6dwii7i88ASe4eY4qNrd6Ir6e36jpn1rWvo5XdVUBw4bHcM/DgfgixdqoDLnrGbsLFFJ2gHbsDlxXVNQ6Tjt1Q8RNDojxbniCO4gqK1lsGTtYGH1RcaKloKDdumY5579zz/AAW2gloaYD2elp4z4hgJ+Z4qw62yA8ZcDyarkVsj/tHyP+OP3ILk12PHLj8Ssf22ol/FMe7zDVsIKCGP3IWA+OMn6rLbTEjllXujSCKulOSAweLnfcq2295/G1B9GjC3raN5HuHCvQ2e4VBxBRzSDnkMOPmeCDRMoKcc2lx83FVmjp8H7IfAlb6ns8GT7ZqDT9vIOC2puLA4fqs3FU19tpafZ7Pf7BcHSODWtpLg1ziT+i7afopsXEefQRfk72+jvvVs0Lwfs6hw8iFtJGOae00tyMjI5q3hUawsr4h2ZQ70cqm19yi5iQDy4rPLeKbEGPFqCtYeMruHmsyDU1UDxld81ZdEx3vAO9RlWnUVOc/ZgH9HITuNq3U1Q4DMp+aty3l8h4vK1Zt8X5L3j45XgonDlMfi1Bmvri78pUNqiB3H1CxvY3/3w/Z/mvPZJP75o/V/mqMh1Y/duyDwxy4K26seXA5GByHcrfsj/wC+/wAv814aJ3fP/k/moLvtji0tOMZyPL0RtWR+UrQoSeInP7P816KHj+OP7KDOhuLmDIer7bxPnLZCcea1oomjh1rz8Aq20sY/KcfimjPku9W/lI75q0a6qecumI+KsiJgHuj48VW1rQOCaa9dNI/3pXlecMeJ8yvcBVd3BBSOeAQPQL0gnhkr0eaqbxcG8AScDJxk+Co8x3LwhXq2W3WyiFXcaib8c2MwQR7nlpBO8EkNA4EeOVWdUdGxh2+x6w6z8/raXHy2fxU07MTaO7gfJUujBC3mlKPSup5hT0WsqO1Vbs7YLxA+Bp8B1rN7c+oCk7+iTWb43SWqlob7G3m61V8VSf2Q7f8A5U7I50WEcvuQmUDgSFurxYLzZ5jDdrVXUEg4FtTTuiP+YBa8xOxxCKxOvlb4H1WHW1r+LSSPitqYzywrEtGx/vRtPq0K9xGZniR6kel300ZHXPa0eZwrkNqgL/xEfH9EKUacsTXzN2RNBP5rcLOLIyaF00VFXV1M6SKhgp3yzuOWhzQOIA784HlwC4WeJyu39NV2pbBpaPSdNxuFftlqiP7KEHIB83EA+g81xA81JGa8REVQREQEREBbC3Xq629rWUtdMyNr94iLtzN3iWngVr0QbqXVF6llMj6snJyQGgD6K9PqieahkpZrbb5XSDBme2Rzx6Zdj6KPohoiIgKdW3pMuNBbYqGDT+nw2Jm1rxTyMceHM7ZACfPCgqIJVcekHVlbBJT/AIVfTQPdu2U7BHj0cO1j4qLve6R7nvcXucclzjkkqlEBERAREQEREBERB2joy1jbrxYYtO36qjp66lbspaiU4bLH3MJ7nDkPELPvFjmheXbBtPI9xXCFJNL661bpphist/raWFxy6ISbmE+O05CRdTo2meR21jC4nkGjKyRpypgYZa0R0UYG7dVSNhGP1yM/BQy+9KOvLxSOo6zU1d7O73o4ndWHeu3Ch00skry+WR8jjzLnZKumurSXbR9C1rqm9ipcfejo4HSOHxdtb8nFaubpBtUAIodPPmeHdl9VU4aR5sYAR+0udrxREurOkLUkrpPZJKS3RvPu01M0Fvo92Xj5qP3W63O6zddc7jV1sn508znkfMrBRB7wWTaqU1lyp6Qf2sgb8ysbK2GnpYoL3STzlwhZKC8t5geKDol0la2rggZwhgYZXN7trRhoPllaOCsecQ9UZZ3ytazDsDicY5fVbi7MofZp6qnu9JWS1D2sEMDi4xsA3EuyOHHAx6rSUDoYn1k8kjOsp6R7qeNziC+V/YbjzbuL/wBVXVbSufZmVUkVs1BRXKNjXOMjWvgOBz7MgHwAJJVhjmubua4OHiDkKGSQspo+rHbmd7xHcPJW4qiamdmCVzHd+08FBOUWu03JdLhDNNNDGKWnaHT1TzsZE08i4+Z4ADie4FbKF1NUl3sNZBWBoJPVEh2B3lrgHfRaHi8JXrgWkgjBHMeCpKK9ym5UErzcPFBWXJuKtlw8V5vQXcpuVvcvdyC5leqgHKqHPJOApRU3HevSQAsp1vlggZU174rfTP8Admq39W13DPZB7Tv1QVrLjcrC8NprZd5ZKkjjLNSdXCT4NJdn4uAHooL0kjWNLnODWjmScBXdOVNgr7q6luN+itkDIXymd0D5Q4tGRG0NxlzuQyQ3PMhQm7ivjqS2tdI92cYdnHy7lixO2nezjjmO8IiXXPUVqqKuOKw0tbC2LdulrXseZ+PZOxrQGYGezl3qrVtfLNBMwEulb9uzx3N4n5jK09AKV1U2WUloLHB21oJzjsnHDvx8FtrBPHTXOnnla50TJAZWtPEtz2gPhlBt79DPX6YqpqYboxCJJeXBgIcD8DgfrFc4XTtY3S12q23TS9tjqd7pBG+aoY3IiB3ANx+dwJK5k4YcQEL5eDgchZtqutytVUKq219TRzjlJDIWu+YWEiI7Jo3+kl0n6fpm0NVc4b9QDnT3SETZHhuPFTK3dPfRlf5gzXPRJboC89qqtDjC8eJw0tyvmlEH2ZZdJ/0fdc0wn0zr2qsk7h/4aukYSzyw8A/5lVVf0brjLGKmxasst0pj7r8PZn9ncPqvjIEg5BwtpaNR3+0Ai13q4UQPMQ1DmA/AFNNfUlX0JXazU8lZeLpZqSlhaXSSvqHYaB+qudX3pL05pnrKXTMX4arA0htXIwx07HeIB7T/APKuPXLUF9uQIuF4r6oHmJahzh9StblF2sq7XCsutxnuNwqH1FXUPL5ZHnJcSsRERBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAV6ndtOfBWVVG173NjY0uc47QBzJPcgl9igaLL7Xs2umecnyC1VVUnrpMHmck+AUru9N+DrPT0We1HE2Mk8OPf/FQWoPW1DmRZIc7h5+aLFEkhe/YzPaPPvKkFosMVPbRer9K6kthcREAPtapw5siaeeO9x7Le/Jw05NNbrfpu1091vkTaqsqWiSituSOsYeUspHFsfgBhz/JvEx+9XW4Xmu9tuVQZpQ0MYMYZEwcmMaODWjuAwAgvX2/1dzYyljYKO3RHMNHETsb+k789/i48fQcFqMHORwKu4Xu1EZtJfblA7tzCpbnJbON2eGPe976rZUupKchraqmmYfynxuDs+jTj96jpavMIJrBdtOStJkudZAe4OoA7PykWur71TQ1ksVMHVELXEMlxs3juO08R6KPxkte1xHevJnbpHuxjLiUWN9S3iKZ5bIOpAHBzjkE+HBX5bjTsDvt43YaSMHOTjkovGeaqPun0RW5F+zypj+3/ACUgrayx29tAaqoubjVUUdS7q6VmGOdnLQS8bgCCM8PRQRp4LeXtrptP6fqiQQIpqX02SF2PlKERnu1JaYpCY6KuqW92+RkXzwHLGk1lcmU/U0NLRUTsn7dkW+Yg9255OPVoC0cjMK3t48kRVWVNVWzmesqZqmUjBfK8vcfieKtjlhVlpXm1Bm0VbgCGuMktPjaCOLmDuxnmPL5YVFTSGNgqKdxkhPEOHd/1/wB1jhXqGpkpZg5oEkZOXxuPB33HzQUMeSctOHfvW6ssnWPaccQcEeYWBcaeCRntVCXGE+81w7TfEHHePrz8hcslQMhjvfadwPiPBFbPpChmbV0dY45ZPTtjB84xt/8AbtUSPNdL1XSfhDQXtLOMlDKH8BzaeB/fn4LmiIIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgKQ9HtB7fqqlDm5ip8zyeQbxH1wo8ug9GNMyls9fdX7d8rhAzPMADLvnkfJBTr2s3TPaDxJPLz/ktZo2ipg2svlxibJQ26LrpI3HAmcTtji8e08jOPyQ49yxdSVLqmtO3jk8Pj/JXdQS+xaboLOzIdUv9tn4DiACyIfLrD+sEVpblX1VzuE9wrpTLUzvL5HHx8B4AcgO4DCsZVGUBRF5oVbR5K1EJZHhsbSSTgDGcldBb0MdJL2hx01UsBHJ9RE0j1G7gggoj3dyq9nIPEYU9Z0J9Iv8A5bIPnXRf8yuf6kOkdxx+AYm58a6P/mRcQCan+zBaQePFYBJW9uOktS22OWesslxghhz1kr6d4Y0A4zuxjHmsS80EFI6nEW/t08cjtxz2nNBP70GtZzKrBXnIYXg4IqrYcZHILe0zRU6Na3JMlLcxgeDZY+P1iC09KXNmaW8SeGMcx4KQWsRxW+opWMa1lQWue45OC3OCOPDmfmiNXJTnwVsw48VuhLbmnDqyHI8RlePNpkI3V8I8gEMaQx+CtOZhb+50FPFSRVtLO2aCRxZuac4cO4+BWlkLSeyQURjlqp71ccrbkF+imEM7dxwxxw7+BVUrRSXEObwZncMfmn/orEdxCy35mt7JjxdG7afMf9fvRY6ZoiSCtpZrXVdqKpjMLhnHMcFyu40slDcKijlxvgkdG4jvIOMqV6RrnRSQuDuPL4j+Ss9KNNi+R3NjT1dbEHF2Bje0AOA+G0/FWlRJERRBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQegZOBzXRnt/BWl6SgBw/Zl+Rg7ncT8uXwUJ01SCtvlLA9pdHv3PAP5I4n6BSbV1X1krhu5+Hn/ACVWNPaaV91v8NPGcGWQAHntycAn0HH4LD1LWMr77VVMIYIN+yEMGB1bRtb9AFtbG51DY7leA7bIGdRCQ7Dg+TLcj0YJPoox3KFep3FeBe9yI6B0a0lhjZS3C5RSVdWZ2thhJ2xRgOH2jscXHwHAcO9dSvElJAXhl/rXHJGfaCSfquE0NVJBDBG0ng0Hh58VXJcqqT3pnH4qtSuhXa8Txbupvlb/AMc/eorcdR3VoIbeKw/75yj8k8j/AHpXFWXbc8TlQ1k1l8u9S0smuFTMxwwWvkLgfgV5dpWyvZHLmGWGNkT45AQ5pY0NII7uSwntDRuHcvpOlOmLL0RVmrq7RNp1Fc6nVdVSf1xxbwcS7JcO4BnAeeU3B8zljDx66P6/cvNrf71n1+5dzh6QdNyUsdSehnRQjkLQAZ3tOXcu7/svaXpE0PNUGKXoY0q7Y9ok6uqkBALg0kdnB4lZ90o4WBjB61vA+KyJayWWLqsgAntHvcvvS+dGPRPaLdV3Gu0jaIKWkjdLNIY3dlrRknGeJ8B3nAXyzrTW9hZcZo9OaD09Q0+fsxLA6WUDuLiXbc+QGPVWXRy1kTDz2rJip4CRkM+akserb21++OhtUQ7mi3R4+oypRpHpTlpLhDDe9OWWupi4B7W04ieR34cOAPhkEKqglqoo/bZGGSdsQa17RFKW9orK1db2RU9BXwRBglMkMh73OYGnJ88O+inHT+LbSdIkdVpujgZQVtpo6prQNmd7CQcDkcYz5qK3WokqdB0z5oWxujukoGHZzmFmf3BEuYhkowrJWTMFjORlSsm3v7TqdzgGSjHHuKxiEa4se14/JOUG1s0ropXM47gd2PMc/p+5SbU8bbhpN0g29ZSuErSc5LTwIHzB/VUUe8R1rKluSx4D/Xx+mfmpnp6SN7HU0zndU4OikLcZLHDBxnyJVVzhFfuFLLRV09HOxzJYZHRvaeYIOFYUQREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREEq0FTge2V7wOw0RMPeCeJPyH1WLe5XTzkA8XHh6ngPoPqt3SR+waUpofdklBkdkYOXfyWrsNCbvqKnpdwjje/L3nkxve4+QaCfgqr3Vz20VktFlYMP2GtnyO+QARjPh1bWu/XKjBWdfq78JXmrrtjY2yyEsY3kxvJrR5AABYSiPAve4ove5BJrXTxmjjkkwXGLh8lqurdzwfktlYZy+njgAyAMZ8PJZPVDHJqLjRlj/AoWP8AA/JbvY3P5PyXhDB3D5IrRSNcBxacYXXqS9T1v9GyWizur6bVrZnF35XWU7zk/Jy5tOWhpPD5LrnRPoC8616L7wy11VHSPdeKd8T6rd1buqikDx2QTn7ZvyUvhrhnum+Ec03VzwWu3Qx0NRMx1NEC9rjgce7DTg93wKztRXSatsr6aW1eyBksBEm05OJWjBOB/wBwVOKHoa1Nb6KGlfW2updAwRvdTzVDgCPSA49MrKj6HNRV9pbRw3OymIzsc+d9TK+Rm17XOaWmFpzge6cc14/0uXvlxzy66T/ScqKiLovrI4chstdBHNj8zcXfLc1q+MJcMmkfIDni55HPnyX3zrO00eqNPXGyVhMcNawtDwMmJwIcx482uAOO/kviXpI0neNK3+agu9I6Fzh2XNBLJBng+M/lN+vHBwRheueG5m90QqKqo6xz4mgRB2ACwH5rIhLahjJC0NO7GM8iP4LEMLs4D4yPHrAP5qRaO09cr9cWW+1Uzp3tBkkceyyNve97jwYwAcz9wVjXOzyknTH2L/ZY+9unLYMf7gH+K0lyaB0bUsmOLrxMPlBF963fTY6KTWEctvlbWW6mt9DQNq4/ce+OnDTj9knyWkuhP+rO3txwN5qTn/cQpLL4c91D5uSxXLLmHZWM5VFBCpI4qsqk80GZT5fby4EF0L8geX/X7lINO1GOrOe7Z8RxH0UZoJBHUbXHsPG1wW0tL3QyviJ7TTkerf5fuVixc17TtZd46pjY2tqIg4hhJ7Q7JJz3nGfio6p3qeAV2mDMwPc+mcJWhrc9k8HEnw935KCKIIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICy7RRvr7nT0bBkyyBp9O/wCmViKWdGlGJblVV78baSHhn853AfTKDYarmb1vVMJDWja0Hu7h9FraCRtBpq53MPLJp8UtPtdgjfncfTq2uaf8YVi91bamrcxjsvc7GPXgPomsZWwwW2zsDgaWEzTZGPtJMH5bBH8cotR0cl6iIgvQO5AF6OaCQ6Lmtsdc2muUklO17wWzhu5o8nDmB5jl4FbP8HXGRgkioqh7HcnNicQfjhRejbucApDS00BY0vnmGOQDiAi6um0XY/8A6+r/AOE5UPtN0A40VQPVhWWyOPGGzTYHi4pIxpGBI/4koMBtluMsrY308kbXuDS9zeDR4lfVH9F+nfbui00r5Wvcy71QL2jg7GwZ+i+YWOfG/AkOPVdE0B0mXrSlldaaaG3VEDqh87TUMk3NL8bhlruIyM8u9KsfSslxbHTx02Hh0LNsrWkgtd+dw8Tk+ecrKo3EudVkFgmY0Dc3BfjPax8cA+R8FwM9M15keyR9rsD3s91zmTZb6EngknTbqBzy59utDiTxdumJPzKzivoTrx4rS6krNL1lJLbdQ/g2qga8NfT1TBJtcW7hhuCQdpByPmuKv6b7s08LZb3ejZf+ZYNf01Tytc2bTFBNueHu354uAwHc+YAxlUdGi0J0NTXANjscD6hxw2BklUdxABIDAePAgkDkFJHS6Tt1imslght1JHUU73impYNoeA3jvwPeweTjuweS4X/rrlw1jtKWrawlzSC4OaTjJBznPAfJZVD0t2urqIhV6ZoaIt3NZUQRjdHuAa4+JyAAc5XLqy3hZPoxz78bIyek7SQuOk3sthjgdSzCqET3sjj4Ahx3Oxt7JJxnHDguN6mdHT6TttsFVBLWR19RPKyGZsjWxujia05aSMktdwXeNUahsk+jrjJFW0lTvpnsZHvB3OIwBhfMTx9q7stbx5BeT4XOpOhnU8683pJynTzkoc7s4KsuVyRWSV9F6XhVJXpPFeEoAJaQ5vAtOQtoyZvXx1TBgPGSPAju+S1JKzaE7qWVue1GQ9owixNbKY6imlopcOY9pjILsZDuSgFXA+mqpaeTG+J5Y7HLIOFJtN17XVTYwCCG7Tnv8PuWNr2kMV4bVjJZVxh+duBuHAj6A/FCo6iIiCIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiIC6Jp2B1v0M3YD7TcZOyCPE7W/Dv+K59EwvkYwEDcQOK6tSMbLcKSnY3EFDDuA8/db/E/BFjCk0vaaeriqpJXsYJAZHOcS3aBueT+q1xXP7tWOuN1qq90Yj9omdIGA8GAnIaPIDh8F0XXFXNSafqZot7RKRRte0jG543yD9gNH665hhEF6AvQF6g8AXoREGVSO2uC3NPUcAtBGcFZsEmBzQb1lQcc0fOcc1rWTDHNVGYeKDM63vyqm1hYO9a8y+a8MgQbMXLyK9FzPLBWp6wJvGEG3/CGeSty1ZeOa1Rk8151h8UGcZOPNeiQgcCsHrPNDL5oMt8pDTg4zz4rUyu+0KvSS8OaxXnLkFEhVo81eKoICC0irIXmEFBCu0khhqY5AAcEcCMgqjCpIQdWu1LBUWVlVRQxx9hs8YY0DGOOPlkLSatgbXaUFSxoLqZ7ZQ7PEMd2XAD1LPktnoSubW6eMDyC+ndxBOey7+efmvaWnLbfd7cW7uqglwCM4jLCQfgO9GvLlyL3uXiMiIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiILkZLXtcBktOV120XOw1NuimgqYKOeRrTUiWQ8HAY4Z449Fx8EhVtlcO8oJf0kXqhulzbR2hkrLVSOeYTMQZJnuxukfjgM7QAByAA481EHI6QlUlxQer0KjJTJQXEVvJTJQX2lXGvx3rF3FN5QZolx3qrrfNYG8r3rHIM/rvNOtWB1hTrCgz+tTrR4rA6xydY5BnGQLzrB4rC6wpvKDM63zXhk81h7ym8oMveD3qlxCxt5Xu8oL5K8Ksbym8oLxwqSQre4rzcgukrwEZVvJTKCRaSvEVpnqGVEAmpapgZJt4PjwQdzT8OI71I9SaxpTYJLbZXTB9Swx1E72hrurPNg4kkHHHPyXOw8jkheSi6OCpXuV4iCIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiD//Z"

print("Conectando al Solo...")
vehicle = connect('udp:0.0.0.0:14550', wait_ready=True, heartbeat_timeout=30)
print("Conectado")

following = False
target_lat = None
target_lon = None

def telemetry_loop():
    while True:
        try:
            loc = vehicle.location.global_frame
            socketio.emit('telemetry', {
                'lat': loc.lat or 0.0,
                'lon': loc.lon or 0.0,
                'armed': vehicle.armed,
                'mode': vehicle.mode.name,
                'battery': vehicle.battery.voltage or 0.0
            })
        except:
            pass
        time.sleep(1)

def follow_loop():
    global following, target_lat, target_lon
    while True:
        if following and target_lat and target_lon and vehicle.location.global_frame.lat:
            try:
                import math
                dlat = target_lat - vehicle.location.global_frame.lat
                dlon = target_lon - vehicle.location.global_frame.lon
                dist = math.sqrt((dlat*111320)**2 + (dlon*111320)**2)
                if dist > 5.0:
                    point = LocationGlobalRelative(target_lat, target_lon, 2)
                    vehicle.simple_goto(point)
            except:
                pass
        time.sleep(2)

threading.Thread(target=telemetry_loop, daemon=True).start()
threading.Thread(target=follow_loop, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Violeta - Control de Misión</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>


    <style>
        :root { 
            --violeta-main: #5924a8; 
            --white: #FFFFFF; 
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body, html { height: 100%; width: 100%; overflow: hidden; font-family: 'DM Sans', sans-serif; background: var(--white); }

        /* --- INTRO (Fondo Blanco) --- */
        #intro-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-color: var(--white);
            display: flex; justify-content: center; align-items: center; z-index: 500;
        }
        .intro-content { text-align: center; }
        
        .drone-icon {
            width: 130px; height: auto; opacity: 0;
            filter: invert(19%) sepia(51%) saturate(3665%) hue-rotate(248deg) brightness(91%) contrast(93%);
            animation: drone-approach 2s ease-out forwards, drone-ellipse-exit 1.5s ease-in-out 2.8s forwards;
        }
        
        .intro-title {
            color: var(--violeta-main);
            font-family: 'Playfair Display', serif;
            font-size: 5rem; font-weight: 900; letter-spacing: 10px;
            opacity: 0; margin-top: -200px;
            animation: title-appear 0.8s ease-out 3.8s forwards;
        }

        /* --- LAS PAREDES (CORTINAS) --- */
        .curtain {
            position: fixed; top: 0; width: 50%; height: 100%;
            background: radial-gradient(ellipse at 60% 0%, #C9A8DC 0%, #9B72C0 25%, #5B2D8E 55%, #3B1A6B 100%);
            z-index: 600;
            transition: transform 1.2s cubic-bezier(0.65, 0, 0.35, 1);
            transform: scaleX(0);
        }
        #curtain-left { left: 0; transform-origin: left; }
        #curtain-right { right: 0; transform-origin: right; }
        .curtains-closed { transform: scaleX(1) !important; }
        .curtains-open-left { transform: translateX(-100%) !important; }
        .curtains-open-right { transform: translateX(100%) !important; }

        @keyframes drone-approach { 
            0% { opacity: 0; transform: scale(0.3) translateY(40px); } 
            100% { opacity: 1; transform: scale(1.2) translateY(0); } 
        }
        @keyframes drone-ellipse-exit { 
            0% { opacity: 1; transform: scale(1.2) translate(0, 0); } 
            30% { transform: scale(1.1) translate(120px, 60px); } 
            60% { transform: scale(0.9) translate(280px, -120px); opacity: 1; } 
            100% { opacity: 0; transform: scale(0.5) translate(650px, -450px); } 
        }
        @keyframes title-appear { 
            0% { opacity: 0; transform: translateY(20px); } 
            100% { opacity: 1; transform: translateY(0); } 
        }

        /* --- APP INTERFAZ --- */
        .app-main-content { 
            display: none; 
            height: 100vh; 
            overflow-y: auto;
            overflow-x: hidden;
            background: radial-gradient(ellipse at 60% 0%, #C9A8DC 0%, #9B72C0 25%, #5B2D8E 55%, #3B1A6B 100%);
        }

        .app-container { 
            max-width: 420px; 
            margin: 0 auto; 
            padding: 40px 22px 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* HEADER */
        .app-header { 
            text-align: center; 
            margin-bottom: 32px; 
        }
        .app-header .greeting { 
            color: rgba(255,255,255,0.85); 
            font-size: 1.35rem; 
            font-weight: 300;
            font-family: 'DM Sans', sans-serif;
            letter-spacing: 0.5px;
        }
        .app-header .name { 
            font-family: 'Playfair Display', serif; 
            font-style: normal;
            font-size: 4.2rem; 
            color: #fff; 
            line-height: 0.95;
            font-weight: 700;
            letter-spacing: -1px;
        }
        .app-header .drone-small {
            display: inline-block;
            vertical-align: middle;
            margin-right: 8px;
            opacity: 0.9;
        }

        /* SUBTITLE */
        .app-subtitle {
            text-align: center;
            color: rgba(255,255,255,0.9);
            font-size: 1.15rem;
            font-weight: 400;
            margin-bottom: 28px;
            line-height: 1.4;
        }

        /* COORDINATE INPUTS */
        .coord-section { margin-bottom: 28px; }
        .coord-row {
            display: flex;
            gap: 12px;
            margin-bottom: 12px;
        }
        .coord-group {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 7px;
        }
        .coord-input {
            width: 100%;
            padding: 14px 16px;
            border-radius: 50px;
            border: none;
            background: rgba(120, 90, 160, 0.55);
            color: #fff;
            font-size: 1rem;
            font-family: 'DM Sans', sans-serif;
            text-align: center;
            outline: none;
            backdrop-filter: blur(8px);
        }
        .coord-input::placeholder { color: rgba(255,255,255,0.4); }
        .coord-label {
            color: rgba(255,255,255,0.75);
            font-size: 0.82rem;
            font-weight: 400;
            letter-spacing: 0.3px;
        }
        .btn-enviar {
            display: block;
            margin: 0 auto;
            padding: 14px 48px;
            border-radius: 50px;
            border: none;
            background: rgba(120, 90, 160, 0.6);
            color: rgba(255,255,255,0.9);
            font-size: 1rem;
            font-style: italic;
            font-family: 'Playfair Display', serif;
            cursor: pointer;
            backdrop-filter: blur(8px);
            transition: background 0.2s;
        }
        .btn-enviar:hover { background: rgba(140, 110, 180, 0.75); }

        /* CARDS */
        .card {
            border-radius: 20px;
            padding: 20px 22px;
            margin-bottom: 14px;
        }
        .card-conexion {
            background: rgba(210, 185, 225, 0.35);
            backdrop-filter: blur(12px);
        }
        .card-keyword {
            background: rgba(100, 70, 140, 0.5);
            backdrop-filter: blur(12px);
            text-align: center;
        }
        .card-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            color: rgba(255,255,255,0.85);
            font-weight: 400;
            margin-bottom: 10px;
        }
        .card-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: rgba(255,255,255,0.75);
            font-size: 0.92rem;
            margin-bottom: 4px;
        }
        .card-row span:last-child {
            color: rgba(255,255,255,0.9);
            font-weight: 500;
        }
        .keyword-label {
            color: rgba(255,255,255,0.65);
            font-size: 0.85rem;
            margin-bottom: 8px;
        }
        .keyword-word {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 1.8rem;
            color: #fff;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .keyword-word::before { content: '"'; }
        .keyword-word::after { content: '"'; }
        .keyword-desc {
            color: rgba(255,255,255,0.6);
            font-size: 0.8rem;
        }

        /* BOTTOM ACTION SECTION */
        .action-section {
            display: flex;
            gap: 12px;
            margin-bottom: 0;
            align-items: stretch;
        }

        /* Pánico box - cuadrado izquierda */
        .btn-panico-box {
            flex: 0 0 auto;
            width: 130px;
            background: rgba(180, 155, 205, 0.3);
            border-radius: 20px;
            border: none;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 18px 12px;
            color: #fff;
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem;
            font-weight: 400;
            transition: background 0.2s;
        }
        .btn-panico-box:hover { background: rgba(200, 50, 50, 0.35); }
        .btn-panico-box.panic-active {
            animation: panic-pulse 0.5s infinite alternate;
        }
        .alarm-emoji { font-size: 2.4rem; }

        /* Botones derechos */
        .right-buttons {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .btn-action {
            width: 100%;
            padding: 16px 18px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            font-family: 'DM Sans', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            letter-spacing: 0.2px;
            transition: opacity 0.2s, transform 0.1s;
        }
        .btn-action:active { transform: scale(0.98); }

        .btn-armar {
            background: rgba(100, 80, 130, 0.7);
            color: #fff;
            backdrop-filter: blur(8px);
        }
        .btn-detener {
            background: rgba(200, 185, 215, 0.4);
            color: rgba(255,255,255,0.9);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .btn-detener .stop-icon {
            width: 18px; height: 18px;
            background: rgba(255,255,255,0.7);
            border-radius: 3px;
            flex-shrink: 0;
        }
        .btn-emergencia {
            background: rgba(60, 40, 90, 0.8);
            color: rgba(255,255,255,0.9);
        }

        @keyframes panic-pulse { 
            from { background: rgba(200, 50, 50, 0.4); } 
            to { background: rgba(255, 0, 0, 0.7); box-shadow: 0 0 30px rgba(255,0,0,0.5); } 
        }

        /* LOG BOX */
        .log-box { 
            background: rgba(0,0,0,0.25);
            border-radius: 0;
            padding: 16px 22px; 
            color: rgba(255,255,255,0.45); 
            font-size: 0.78em; 
            min-height: 90px;
            overflow-y: auto;
            margin-top: 18px;
            margin-left: -22px;
            margin-right: -22px;
            flex: 1;
        }
        .log-box p { margin-bottom: 3px; }

        /* GPS dispositivo */
        .device-gps-label {
            text-align: center;
            color: rgba(255,255,255,0.4);
            font-size: 0.75rem;
            padding: 4px 0 2px;
        }
    </style>
</head>
<body>

    <!-- INTRO -->
    <div id="intro-overlay">
        <div class="intro-content">
            <img src="static/dron_icono.png" class="drone-icon" alt="Dron Violeta">
            <h1 class="intro-title">VIOLETA</h1>
        </div>
    </div>

    <!-- PAREDES DE TRANSICIÓN -->
    <div id="curtain-left" class="curtain"></div>
    <div id="curtain-right" class="curtain"></div>

    <!-- APP -->
    <div id="app-content" class="app-main-content">
        <div class="app-container">

            <!-- HEADER -->
            <div class="app-header">
                <div class="greeting">hola, soy</div>
                <div class="name">
                    <svg class="drone-small" width="52" height="36" viewBox="0 0 110 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="15" cy="15" r="7" stroke="white" stroke-width="4"/>
                        <circle cx="95" cy="15" r="7" stroke="white" stroke-width="4"/>
                        <circle cx="15" cy="65" r="7" stroke="white" stroke-width="4"/>
                        <circle cx="95" cy="65" r="7" stroke="white" stroke-width="4"/>
                        <line x1="15" y1="15" x2="35" y2="33" stroke="white" stroke-width="3"/>
                        <line x1="95" y1="15" x2="75" y2="33" stroke="white" stroke-width="3"/>
                        <line x1="15" y1="65" x2="35" y2="47" stroke="white" stroke-width="3"/>
                        <line x1="95" y1="65" x2="75" y2="47" stroke="white" stroke-width="3"/>
                        <rect x="32" y="30" width="46" height="20" rx="7" fill="white" opacity="0.9"/>
                        <circle cx="55" cy="40" r="7" fill="rgba(103,58,183,0.6)"/>
                        <rect x="46" y="50" width="4" height="8" rx="2" fill="white" opacity="0.7"/>
                        <rect x="60" y="50" width="4" height="8" rx="2" fill="white" opacity="0.7"/>
                    </svg>Violeta
                </div>
            </div>

            <!-- SUBTITLE -->
            <div class="app-subtitle">
                Estoy lista para acompañarte.<br>¿A dónde vamos hoy?
            </div>

            <!-- COORDENADAS -->
            <div class="coord-section">
                <div class="coord-row">
                    <div class="coord-group">
                        <input id="inp-lat" class="coord-input" type="number" step="0.000001" placeholder="">
                        <span class="coord-label">Latitud</span>
                    </div>
                    <div class="coord-group">
                        <input id="inp-lon" class="coord-input" type="number" step="0.000001" placeholder="">
                        <span class="coord-label">Longitud</span>
                    </div>
                </div>
                <div id="device-gps" class="device-gps-label">GPS dispositivo: --</div>
                <button class="btn-enviar" onclick="sendCoords()">Enviar destino</button>
            </div>

            <!-- MI CONEXIÓN -->
            <div class="card card-conexion">
                <div class="card-title">Mi conexión</div>
                <div class="card-row">
                    <span>Batería</span>
                    <span id="bat">--</span>
                </div>
                <div class="card-row">
                    <span>Modo</span>
                    <span id="modo">--</span>
                </div>
                <div class="card-row">
                    <span>Estado</span>
                    <span id="estado">Desarmado</span>
                </div>
                <div class="card-row">
                    <span>GPS</span>
                    <span id="gps">Esperando...</span>
                </div>
            </div>

            <!-- PALABRA CLAVE -->
            <div class="card card-keyword">
                <div class="card-title">Nuestra palabra clave es...</div>
                <div class="keyword-word" id="keyword-display">KEYWORD</div>
                <div class="keyword-desc">Si la dices, activaré el protocolo de emergencia de inmediato</div>
            </div>

            <!-- ACCIONES -->
            <div class="action-section">
                <!-- Pánico -->
                <button class="btn-panico-box" id="btn-panic" onclick="panic()">
                    <span class="alarm-emoji">🚨</span>
                    <span>Pánico</span>
                </button>

                <!-- Botones derechos -->
                <div class="right-buttons">
                    <button class="btn-action btn-armar" onclick="arm()">Armar y Despegar</button>
                    <button class="btn-action btn-detener" onclick="stopDrone()">
                        <span class="stop-icon"></span>
                        Detener
                    </button>
                    <button class="btn-action btn-emergencia" onclick="emergencyLand()">Aterrizaje de Emergencia</button>
                </div>
            </div>

            <!-- LOG / COMANDOS -->
            <div class="log-box" id="log">
                <p style="color:rgba(255,255,255,0.25); font-style:italic;">Los comandos aparecerán aquí...</p>
            </div>

        </div>
    </div>

    <script>
        const socket = io();
        let sirenOn = false;
        let audioCtx = null;
        let sirenInterval = null;
        let panicActive = false;

        // ── INTRO TIMELINE ──────────────────────────────────────────────
        const cLeft  = document.getElementById('curtain-left');
        const cRight = document.getElementById('curtain-right');
        const intro  = document.getElementById('intro-overlay');
        const app    = document.getElementById('app-content');

        setTimeout(() => {
            cLeft.classList.add('curtains-closed');
            cRight.classList.add('curtains-closed');
        }, 5800);

        setTimeout(() => {
            intro.style.display = 'none';
            app.style.display = 'block';
            cLeft.classList.add('curtains-open-left');
            cRight.classList.add('curtains-open-right');
        }, 7000);

        // ── AUDIO (sirena) ───────────────────────────────────────────────
        function initAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        function playSiren() {
            initAudio();
            sirenInterval = setInterval(() => {
                const osc  = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                osc.frequency.linearRampToValueAtTime(1400, audioCtx.currentTime + 0.4);
                gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
                osc.start(); osc.stop(audioCtx.currentTime + 0.4);
            }, 500);
        }
        function stopSiren() {
            if (sirenInterval) { clearInterval(sirenInterval); sirenInterval = null; }
        }

        // ── LOG ──────────────────────────────────────────────────────────
        function addLog(msg) {
            const box = document.getElementById('log');
            const placeholder = box.querySelector('p[style*="italic"]');
            if (placeholder) placeholder.remove();
            const p = document.createElement('p');
            const time = new Date().toLocaleTimeString('es-MX', {hour:'2-digit', minute:'2-digit', second:'2-digit'});
            p.textContent = '[' + time + '] ' + msg;
            p.style.color = 'rgba(255,255,255,0.6)';
            box.appendChild(p);
            box.scrollTop = box.scrollHeight;
        }

        // ── SOCKET EVENTS ────────────────────────────────────────────────
        socket.on('telemetry', data => {
            document.getElementById('gps').textContent =
                (data.lat || 0).toFixed(6) + ', ' + (data.lon || 0).toFixed(6);
            document.getElementById('modo').textContent = data.mode || '--';
            document.getElementById('estado').textContent = data.armed ? '🔴 Armado' : '🟢 Desarmado';
            const pct = data.battery
                ? Math.max(0, Math.min(100, ((data.battery - 15.2) / (16.8 - 15.2)) * 100)).toFixed(0) + '%'
                : '--';
            document.getElementById('bat').textContent = pct;
        });
        socket.on('log',       msg => addLog(msg));
        socket.on('panic_on',  ()  => { playSiren(); document.getElementById('btn-panic').classList.add('panic-active'); });
        socket.on('panic_off', ()  => { stopSiren(); document.getElementById('btn-panic').classList.remove('panic-active'); });

        // ── ACCIONES ─────────────────────────────────────────────────────
        function arm() {
            initAudio();
            socket.emit('arm', {});
            addLog('⚡ Armando y despegando...');
        }

        function sendCoords() {
            const lat = parseFloat(document.getElementById('inp-lat').value);
            const lon = parseFloat(document.getElementById('inp-lon').value);
            if (isNaN(lat) || isNaN(lon)) { addLog('⚠️ Ingresa latitud y longitud válidas'); return; }
            initAudio();
            socket.emit('follow', { lat, lon });
            addLog('📍 Enviando destino: ' + lat.toFixed(6) + ', ' + lon.toFixed(6));
        }

        function stopDrone() {
            socket.emit('stop');
            addLog('⏹ Deteniendo...');
        }

        function emergencyLand() {
            socket.emit('emergency_land', {});
            addLog('🛬 Aterrizaje de emergencia activado');
        }

        function panic() {
            initAudio();
            panicActive = !panicActive;
            socket.emit('panic', { active: panicActive });
            addLog(panicActive ? '🚨 ¡PROTOCOLO DE PÁNICO ACTIVADO!' : '✅ Pánico desactivado');
        }
    </script>
</body>
</html>
"""

from flask import send_from_directory, send_file
import os

@app.route('/')
def index():
    kw = random.choice(KEYWORDS)
    page = HTML.replace('KEYWORD', kw)
    return page

@socketio.on('arm')
def handle_arm(data):
    import time
    vehicle.mode = VehicleMode('GUIDED')
    time.sleep(2)
    vehicle.armed = True
    time.sleep(3)
    vehicle.simple_takeoff(2)
    socketio.emit('log', '🚁 Despegando a 2m...')

@socketio.on('follow')
def handle_follow(data):
    global following, target_lat, target_lon
    target_lat = data['lat']
    target_lon = data['lon']
    vehicle.mode = VehicleMode('GUIDED')
    following = True
    socketio.emit('log', f"📍 Siguiendo: {target_lat:.6f}, {target_lon:.6f}")
    socketio.emit('target_update', {'lat': target_lat, 'lon': target_lon})

@socketio.on('panic')
def handle_panic(data):
    if data['active']:
        socketio.emit('panic_on')
        socketio.emit('log', '🚨 PÁNICO ACTIVADO - Alertando área')
    else:
        socketio.emit('panic_off')
        socketio.emit('log', '✅ Pánico desactivado')

@socketio.on('emergency_land')
def handle_emergency_land(data):
    global following
    following = False
    vehicle.mode = VehicleMode('LAND')
    socketio.emit('log', '🛬 Aterrizando de emergencia...')

@socketio.on('stop')
def handle_stop():
    global following
    following = False
    vehicle.mode = VehicleMode('LOITER')
    socketio.emit('log', '⏹ Detenido - modo LOITER')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
