from django.shortcuts import render,redirect
from .models import Contact,User,Book,WishList,Cart,Transaction
from django.core.mail import send_mail
import random
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def initiate_payment(request):
    if request.method=="POST":
        try:
           
            amount = int(request.POST['final_amount'])
          
        except:
            return render(request, 'mycart.html', context={'error': 'Wrong Accound Details or amount'})

        transaction = Transaction.objects.create(amount=amount)
        transaction.save()
       
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(request.session['email'])),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        user=User.objects.get(email=request.session['email'])
        carts=Cart.objects.filter(user=user,status="pending")
        for i in carts:
            i.status="completed"
            i.save()

        return render(request,'redirect.html',context=paytm_params)
    else:
        pass

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)




def index(request):
    return render(request,'index.html')

def contact(request):
    if request.method=="POST":
        n=request.POST['name']
        e=request.POST['email']
        m=request.POST['mobile']
        f=request.POST['feedback']

        Contact.objects.create(name=n,email=e,mobile=m,feedback=f)
        msg="contact saved successfully"
        contacts=Contact.objects.all().order_by("-id")
        return render(request,'contact.html',{'msg':msg,'c':contacts})
    else:
        contacts=Contact.objects.all().order_by("-id")
        return render(request,'contact.html',{'c':contacts})
        
def signup(request):
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        m=request.POST['mobile']
        p=request.POST['password']
        cp=request.POST['cpassword']
        ut=request.POST['usertype']
        ui=request.FILES['user_image']

        try:
            user=User.objects.get(email=e)
            msg="email already exists"
            return render(request,'signup.html',{'msg':msg})
        except:
            if p==cp:
                User.objects.create(fname=f,lname=l,email=e,mobile=m,password=p,cpassword=cp,usertype=ut,user_image=ui)
                rec=[e,]
                subject="OTP for successfull registration"
                otp=random.randint(1000,9999)
                message="your otp for registrations is"+str(otp)
                email_from=settings.EMAIL_HOST_USER
                send_mail(subject,message,email_from,rec)
                return render(request,'otp.html',{'otp':otp,'e':e})

            else:
                msg="password and confirm password does not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        e=request.POST['email']
        p=request.POST['password']
        
        try:
            user=User.objects.get(email=e,password=p)
            print(user.usertype)
            if user.usertype=='user':
               
                if user.status=="active":
                    request.session['fname']=user.fname
                    request.session['email']=user.email
                    request.session['user_image']=user.user_image.url
                    wishlist=WishList.objects.filter(user=user)
                    request.session['wishlist_count']=len(wishlist)
                    cart=Cart.objects.filter(user=user)
                    request.session['cart_count']=len(cart)
                    return render(request,'index.html')
                else:
                    msg1="Verify your OTP"
                    return render(request,'login.html',{'msg1':msg1})
            elif user.usertype=='seller':
                if user.status=="active":
            
                    request.session['fname']=user.fname
                    request.session['email']=user.email
                    request.session['user_image']=user.user_image.url
                    return render(request,'seller_index.html')
                else:
                    msg1="Verify your OTP"
                    return render(request,'login.html',{'msg1':msg1})

        except:
            msg="email or password is incorrect"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

def logout(request):
    try:
        del request.session['fname']
        del request.session['email']
        del request.session['user_image']
        del request.session['wishlist_count']
        del request.session['cart_count']
        return render(request,'login.html')
    except:
        return render(request,'login.html')

def verify_otp(request):
    myvar=""
    otp=request.POST['otp']
    gotp=request.POST['gotp']
    email=request.POST['email']
    print(email)
    try:
        myvar=request.POST['myvar']
    except:
        pass
    if otp==gotp and myvar==forget_password:
        print("Forgot Password")
        return render(request,'enter_new_password.html',{'email':email})

    if otp==gotp:
        user=User.objects.get(email=email)
        user.status='active'
        user.save()
        return render(request,'login.html')
    else:
        msg="incorrect otp try Again"
        return render(request,'otp.html',{'otp':gotp,'e':email,'msg':msg})

def enter_email(request):
    
    if request.method=="POST":
        email=request.POST['email']
        print(email)
        try:
            user=User.objects.get(email=email)
            if user.status=="inactive":
                rec=[email,]
                subject="OTP for activate your Account"
                otp=random.randint(1000,9999)
                message="Your OTP for Activation is"+str(otp)
                email_from=settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from, rec)
                return render(request,'otp.html',{'otp':otp,'e':email})

            elif user.status=="active":
                rec=[email,]
                subject="OTP for Forget Password"
                otp=random.randint(1000,9999)
                message="Your OTP for Forget Password is"+str(otp)
                email_from=settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from, rec)
                myvar="forget_password"
                return render(request,'otp.html',{'otp':otp,'e':email,'myvar':myvar})

        except:
            msg="Email Is Not Registerd With Us"
            return render(request,'enter_email.html',{'msg':msg})
    else:
        return render(request,'enter_email.html')

def forget_password(request):
    if request.method=="POST":

        email=request.POST['email']
        npassword=request.POST['npassword']
        cnpassword=request.POST['cnpassword']

        user=User.objects.get(email=email)
        if npassword==cnpassword:
            user.password=npassword 
            user.cpassword=npassword
            user.save()
            return render(request,'login.html')
        else:
            msg="New Password & Confirm New Password Does Not Match"
            return render(request,'enter_new_password.html',{'msg':msg,'email':email})
    else:
        return render(request,'enter_email.html')

def change_password(request):
    if request.method=="POST":
        opassword=request.POST['opassword']
        npassword=request.POST['npassword']
        cnpassword=request.POST['cnpassword']

        user=User.objects.get(email=request.session['email'])

        if user.password==opassword:
            if npassword==cnpassword:
                user.password=npassword
                user.cpassword=npassword
                user.save()
                return redirect('logout')
            else:
                msg="New password and confirm New password does not Matched"
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg="Old Password Does not Matched"
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')

def profile(request):

    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.email=request.POST['email']
        user.mobile=request.POST['mobile']
        user.save()
        msg="Profile updated successfully"
        return render(request,'Profile.html',{'msg':msg})
    else:
        return render(request,'Profile.html',{'user':user})

def seller_index(request):
    return render(request,'seller_index.html')
def add_book(request):
    if request.method=="POST":
        Book.objects.create(
            book_name=request.POST['book_name'],
            book_price=request.POST['book_price'],
            book_author=request.POST['book_author'],
            book_image=request.FILES['book_image'],
            book_desc=request.POST['book_desc'],
            book_subject=request.POST['book_subject'],
            book_seller=user.objects.get(email=request.session['email'],)
        )
        msg="Book Added successfully"
        return render(request,'add_book.html',{'msg':msg})
    else:
        return render(request,'add_book.html')
        
def view_books(request):
    user=User.objects.get(email=request.session['email'])
    books=Book.objects.filter(book_seller=user)
    return render(request,'view_books.html',{'books':books})

def book_detail(request,pk):
    user=User.objects.get(email=request.session['email'])
    book=Book.objects.get(book_seller=user,pk=pk)
    return render(request,'book_detail.html',{'book':book})
def edit_book(request,pk):
    if request.method=="POST":

        user=User.objects.get(email=request.session['email'])
        book=Book.objects.get(book_seller=user,pk=pk)
        book.book_subject=request.POST['book_subject']
        book.book_author=request.POST['book_author']
        book.book_name=request.POST['book_name']
        book.book_price=request.POST['book_price']
        book.book_desc=request.POST['book_desc']

        try:
            book.book_image=request.FILES['book_image']
            book.save()
            msg="Book Updated Successfully"
            books=Book.objects.filter(book_seller=user)
            return render(request,'view_books.html',{'books':books,'msg':msg})
        except:
            book.save()
            msg="Book Updated Successfully"
            books=Book.objects.filter(book_seller=user)
            return render(request,'view_books.html',{'books':books,'msg':msg})

    else:
        user=User.objects.get(email=request.session['email'])
        book=Book.objects.get(book_seller=user,pk=pk)
        return render(request,'edit_book.html',{'book':book})

def delete_book(request,pk):
    user=User.objects.get(email=request.session['email'])
    book=Book.objects.get(book_seller=user,pk=pk)
    book.delete()
    msg="Book Deleted Successfully"
    books=book.objects.filter(book_seller=user)
    return render(request,'view_books.html',{'books':books,'msg':msg})

def book(request,bname):
    print(bname)
    books=Book.objects.filter(book_name__contains=bname)
    return render(request,'show_book.html',{'books':books})

def user_book_detail(request,pk):
    flag=False
    flag1=False
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    try:
        wishlist=WishList.objects.get(user=user,book=book,status="pending")
        flag=True
    except:
        pass
    try:
        cart=Cart.objects.get(user=user,book=book)
        flag1=True
    except:
        pass
    return render(request,'user_book_detail.html',{'book':book,'flag':flag,'flag1':flag1})

def add_to_wishlist(request,pk):
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    WishList.objects.create(user=user,book=book)
    return redirect('wishlist')

def wishlist(request):
    user=User.objects.get(email=request.session['email'])
    wishlists=WishList.objects.filter(user=user)
    request.session['wishlist_count']=len(wishlists)
    return render(request,'mywishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    wishlist=WishList.objects.get(user=user,book=book)
    wishlist.delete()
    return redirect('wishlist')

def cart(request):
    final_amount=0
    cart=Cart()
    qty=1
    if request.method=="POST":
        qty=request.POST['quantity']
        pk=request.POST['pk']
        book=Book.objects.get(pk=pk)
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.get(user=user,book=book)
        cart.qty=qty
        cart.amount=book.book_price
        cart.net_amount=int(cart.qty)*int(cart.amount)
        cart.save()
   
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user)
    for i in carts:
        final_amount=final_amount+int(i.net_amount)

    request.session['cart_count']=len(carts)
    return render(request,'mycart.html',{'carts':carts,'final_amount':final_amount})

def add_to_cart(request,pk):
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(user=user,book=book,qty="1",amount=book.book_price,net_amount=book.book_price)
    return redirect('cart')

def remove_from_cart(request,pk):
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.get(user=user,book=book)
    cart.delete()
    return redirect('cart')

def search(request):
    search=request.POST['search']
    books=Book.objects.filter(book_name__contains=search)
    return render(request,'search_result.html',{'books':books})

def validate_username(request):
    username=request.GET.get('username',None)
    data={
        'is_taken': User.objects.filter(email__iexact=username).exists()
    }
    return JsonResponse(data)

def validate_login(request):
    username=request.GET.get('username',None)
    data={
            'is_taken': User.objects.filter(email__iexact=username).exists()
    }
    return JsonResponse(data)
