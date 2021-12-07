import requests, json, discord, datetime

def Load(file, x):
    with open(file) as f:
        try:
            return json.load(f)[x]
        except:
            return None

SellerKey = Load("Settings.json", "SellerKey")

async def Log(client, Channel, Message, Title):
    log = client.get_channel(Channel)
    embed = discord.Embed()
    embed.set_author(name=Title)
    embed.add_field(name=f'‎', value=Message, inline=False)
    await log.send(embed=embed)

def Load(file, x):
    with open(file) as f:
        try:
            return json.load(f)[x]
        except:
            return None

def VerifyUser(userid):
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=verifyuser&user={str(userid)}').json()
    if x['message'] == 'User Successfully Verified':
        return True
    else:
        return False
    
def AddSubscription(userid, license):
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=activate&user={userid}&key={license}&pass={userid}').json()
    if x['success'] == True:
        return True
    elif x['message'] == 'Username Already Exists.':
        return None
    else:
        return False

def DeleteUser(userid):
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=deluser&user={userid}').json()
    if x['success'] == True:
        return True
    else:
        return False

def GetExpiry(userid):
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=fetchallkeys').json()
    for key in x['keys']:
        if key['usedby'] == str(userid):
            a = int(key['expires']) / 86400
            b = int(key['usedon'])
            c = datetime.datetime.fromtimestamp(b)
            d = (c + datetime.timedelta(days=a)).isoformat()
            e = f"{c}"
            return f"**Expiry -> `{a} Days`**\n**Day Used -> `{e.split(' ')[0]}`**\n**Expires On -> `{d.split('T')[0]}`**"

def GetUsedKey(userid):
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=fetchallkeys').json()
    for key in x['keys']:
        if key['usedby'] == str(userid):
            return key['key']

def GetExpiryFloat(userid):
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=fetchallkeys').json()
    for key in x['keys']:
        if key['usedby'] == str(userid):
            a = int(key['expires']) / 86400
            return a
            
def DeleteExpiredUsers():
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=delexpusers').json()

def GenerateLicenses(Days, Amount):
    k = []
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=add&expiry={Days}&mask=XXX-XXX-XXX&level=1&amount={Amount}&format=json').json()
    if x['success'] == True:
        for i in range(int(Amount)):
            k.append(x['keys'][i])
        return k
    else:
        print('[!] INTERNAL ERROR | ERROR : FAILED TO CREATE KEYS')

def GenerateLicense(Days):
    k = []
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=add&expiry={Days}&mask=XXX-XXX-XXX&level=1&amount=1&format=json').json()
    if x['success'] == True:
            return x['key']
    else:
        print('[!] INTERNAL ERROR | ERROR : FAILED TO CREATE KEY')

def DeleteLicense(Key):
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=del&key={Key}').json()
    if x['success'] == True:
        return True
    else:
        return False

def CheckLicense(Key):
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=verify&key={Key}').json()
    if x['success'] == True:
        return True
    else:
        return False

def ExtendUser(userid, days):
    try:
        a = GetExpiryFloat(userid)
        b = int(a) + int(days)
        DeleteUser(userid)
        key = GenerateLicense(str(b))
        DeleteLicense(GetUsedKey(userid))
        AddSubscription(userid, key)
        return True
    except:
        return False

def GetActiveLicenses():
    k = []
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=fetchallkeys').json()
    if x['success'] == True:
        for i in range(len(x['keys'])):
            if x['keys'][i]['status'] == "Not Used":
                k.append(f'`{x["keys"][i]["key"]}`   **Days -> `{int(x["keys"][i]["expires"]) / 86400}`**')
        return k 
    else:
        print('[!] INTERNAL ERROR | ERROR : FAILED TO FETCH KEYS')
        return k

def DeleteAllLicenses():
    x = requests.get(f'https://keyauth.com/api/seller/?sellerkey={SellerKey}&type=delunused').json()
    if x['success'] == True:
        return True
    else:
        return False

def GetNumOfAccounts(file):
    count = 0
    for x in open(file).readlines(): 
        count += 1
    return count

def GetAccount(file):
    x = open(file, 'r')
    return x.readline()

def RemoveAccount(file, account):
    with open(file, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != account:
                f.write(i)
        f.truncate()