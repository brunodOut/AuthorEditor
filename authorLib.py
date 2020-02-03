import re

# fnln -> FIRST NAME, LAST NAME (default)
# lnfn -> LAST NAME, FIRST NAME
#

prefixList = ["de", "da", "von", "von der", "dos", "das"]
suffixList = ["Jr", "Sr", "Jnr", "Snr", "J[uú]nior", "S[êe]nior", "Filho", "Neto", "Sobrinho", "[IVX]+", "Primeiro",
              "Segundo", "Terceiro", "Quarto"]


class Author:
    _params = ["firstName", "lastName"]

    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

    def __setattr__(self, name, value):
        params = self.get("_params")
        if name in params:
            object.__setattr__(self, name, str(value.strip()))
        else:
            raise AttributeError

    def __str__(self):
        return self.lastName + ", " + self.firstName

    def get(self, name):
        return object.__getattribute__(self, name)


class AuthorList(dict):
    _authors = []
    _numAuthors = 0
    _iterPosition = 0
    separator = "; "

    def __setitem__(self, key, value):
        # print("setting",key,"=",value)
        ni = Author(value, key)
        self._authors.append(ni)
        self._numAuthors = len(self._authors)
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    #    def _get(self, key):
    #        return object.__getattribute__(self, key)
    def __getitem__(self, key):
        # print("getitem:",key,"_numAuthors=",self._numAuthors)
        if type(key) == int:
            # print("integer key=",key)
            if key < self._numAuthors:
                ##print("\tReturning!! works for key=",key,"_numAuthors=",self._numAuthors)
                return self._authors[key]
            else:
                raise IndexError(key)
        else:
            # print("non-integer key=",key)
            ret = AuthorList()
            if self.hasAuthor(key):
                for i in self._authors:
                    # print("\tEntering",i)
                    if i.firstName == key or i.lastName == key:
                        if not self._isRepeated(key):
                            # print("Not Repeated")
                            return i
                        else:
                            ##print("\t\tRepeated","lastName=",i.lastName,"firstName=",i.firstName,"str()=",i,"_iterPosition=",self._iterPosition,"_numAuthors=",self._numAuthors)
                            ret[i.lastName] = i.firstName
                            # print("\t\tLOOP ENDING, now ready to re-enter... ret._authors=[", ret._authors,"]\n")
                            # print("\t\tRepeated","lastName=",i.lastName,"firstName=",i.firstName,"str()=",i,"_iterPosition=",self._iterPosition,"_numAuthors=",self._numAuthors)
                            # print("gi->else->else: ret=",ret,"len:",len(ret))
                # print("-----------Returning:", ret)
                return ret
            # print("Raising IndexError")
            raise IndexError(key)

    def _isRepeated(self, key):
        if self._countKey(key) <= 1:
            return False
        return True

    def _countKey(self, key):
        if not self.hasAuthor(key):
            return 0
        c = 0
        for i in self._authors:
            if i.firstName == key or i.lastName == key:
                c += 1
        return c

    def hasAuthor(self, key):
        return key in self.keys()

    def __iter__(self):
        self._iterPosition = 0
        self._numAuthors = len(self._authors)
        return self

    def __next__(self):
        # print("$ __next__: ","_iterPosition=",self._iterPosition,"_numAuthors=",self._numAuthors)
        if self._iterPosition < self._numAuthors:
            ret = self[self._iterPosition]
            self._iterPosition += 1
            # print("__next__->ret=",ret)
            return ret
        else:
            # print("Stopping Iteraction...")
            raise StopIteration

    def __str__(self):
        ret = ""
        for i in self:
            ret += self.separator + str(i)
        return ret.replace(self.separator, "", 1)

    # def __repr__(self):
    #    return self.__str__()
    def __new__(self, *args, **kwargs):
        self = dict.__new__(self)
        self._authors = []
        self._numAuthors = 0
        self._iterPosition = 0
        self.separator = "; "
        return self

    def __init__(self, *args, **kwargs):
        # print("__init__",args,kwargs)
        for i in args:
            if type(i) == Author:
                self[i.lastName] = i.firstName
            if type(i) == AuthorList:
                for j in i:
                    self[j.lastName] = j.firstName
            if type(i) == list:
                for j in i:
                    if type(j) == Author:
                        self[j.lastName] = j.firstName
        for i in kwargs:
            self[i] = kwargs[i]

    def addAuthor(self, lastName, firstName):
        self[lastName] = firstName


def isbetween(ev, m, n):
    return (ev >= m and ev <= n)


def sanitize(s, repl='\t', g1=r"[\w+\.]", g2=r"[A-ZÀ-ß]"):
    ret = ""
    regex = r"(.*?)(" + g1 + r")(" + g2 + r")(.*)"
    p = re.compile(regex)
    ma = p.match(s)
    while ma:
        ret += ma.group(1) + ma.group(2) + repl
        s = ma.group(3) + ma.group(4)
        ma = p.match(s)
    ret += s
    return ret


def listFirstInsensitive(l=list()):
    ret = []
    for i in l:
        tks = i.split()
        s = ""
        for j in tks:
            if isbetween(j[0], 'a', 'z') or isbetween(j[0], 'A', 'Z') or isbetween(j[0], 'À', 'ÿ'):
                s += j.replace(j[0], "[" + j[0].lower() + j[0].upper() + "]", 1) + " "
            else:
                s += j + " "
        ret.append(s.strip())
    return ret


def listToRegex(ll=list()):
    l = listFirstInsensitive(ll)
    ret = ""
    c = 0
    while c < len(l):
        prefix = ""
        suffix = "|"
        if c == 0:
            prefix = "(?:"
        if c == (len(l) - 1):
            suffix = ")"
        ret += prefix + l[c] + suffix
        c += 1
    return ret


def fullAuthorsList(s=str(), sep=','):
    authors = s.split(sep)
    procAuthors = []
    for i in authors:
        tks = i.split()
        lastName = tks.pop().strip()
        firstAndMiddleNames = ""
        for j in tks:
            firstAndMiddleNames += j.capitalize().strip() + " "
        procAuthors.append(lastName + ", " + firstAndMiddleNames.strip())
    authorList = ""
    for i in procAuthors:
        authorList += i + "; "
    return authorList[0:len(authorList) - 2]


def authorsRegex(entrySeparator=',',
                 order="fnln",
                 lastNameSeparator=' '):
    modelRE = r"""([\s]*)((((?!(de|da|dos)\b)\b[\w\.\-]+[\s])+)((de|da|dos)?[\s]+([\w\.\-]+)[\s]+(Jr)?))[,]?(.*)"""
    prefLastNameRE = listToRegex(prefixList)
    sufLastNameRE = listToRegex(suffixList)
    lastNameRE = r"(?P<lastName>" + prefLastNameRE + r"?[\s]*(?:[\w-]+)[\s]*" + sufLastNameRE + "?)"
    firstNameRE = r"(?P<firstName>(?:(?:[\w-]+|[\w]\.)[\s]*?)+?)"
    entrySeparatorRE = r"[\s\.]*?(?:" + entrySeparator + r")[\s]*"
    innerSeparatorRE = r"[\s" + lastNameSeparator + "]+?"
    beginningRE = r"(?:[\s]*?)"
    endingRE = r"(?P<remains>.*)"
    if order == "lnfn":
        nameRE = lastNameRE + innerSeparatorRE + firstNameRE
    else:
        nameRE = firstNameRE + innerSeparatorRE + lastNameRE
    RE = beginningRE + "(:?" + nameRE + ")" + entrySeparatorRE + endingRE
    return RE

def firstEntrySeparator(entrysep):
    print("firstEntrySeparator", entrysep)
    p = re.compile(r"\[(?P<innerList>.*)\]")
    ma = p.match(entrysep)
    if ma:
        print(ma.group("innerList"))
        lst = ma.group("innerList")
        if lst[0] == "\\":
            return lst[1]
        else:
            return lst[0]
    else:
        print("Not a match")
        return entrysep

def readAuthors(s=str(),
                entrySeparator=',',
                order="fnln",
                lastNameSeparator=' '):
    entries = s + firstEntrySeparator(entrySeparator)
    regex = authorsRegex(entrySeparator, order, lastNameSeparator)
    print("regex:",regex)
    p = re.compile(regex)
    ma = p.match(entries)
    ret = AuthorList()
    while ma:
        groups = ma.groupdict()
        #print(groups)
        ret.addAuthor(groups.get("lastName"),groups.get("firstName"))
        entries = groups["remains"]
        ma = p.match(entries)
    return ret

def printAuthor(s=str(), sep=','):
    print(fullAuthorsList(s, sep))

def unescape(s=str()):
    ret = s.replace(r"\t", "\t")
    ret = ret.replace(r"\s"," ")
    #print(ret,ret.endswith("\\"),"\\")
    #if ret.endswith("\\"):
    #    return ""
    return ret