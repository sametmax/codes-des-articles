class BaseConverter(object):
   """ Tool to convert between base 10 and a custom base.

      Example:

         >>> base4 = BaseConverter("0123")
         >>> base4.from_base_10(9)
         '21'
         >>> base4.to_base_10('21')
         9
         >>> symboles = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
         >>> crockford_b32 = BaseConverter(symboles)
         >>> crockford_b32.from_base_10(100000)
         '31N0'
         >>> crockford_b32.to_base_10('31N0')
         100000
   """

   def __init__(self, symboles):
      if not symboles:
         raise ValueError('symboles can not be empty')
      self.symboles = symboles
      self.sym2val = {l: i for i, l in enumerate(symboles)}
      self.val2sym = dict(enumerate(symboles))

   def to_base_10(self, string):
       """ Convert from the custom base to base 10 """
       i = 0
       base = len(self.sym2val)
       for c in string:
           i *= base
           i += self.sym2val[c]
       return i

   def from_base_10(self, number):
       """ Convert from a base 10 to the custom base"""
       array = []
       base = len(self.val2sym)
       while number:
           number, value = divmod(number, base)
           array.insert(0, self.val2sym[value])
       return ''.join(array) or self.symboles[0]

   def __repr__(self):
      # fixme:  remove non ascii chars
      return '<BaseConverter %s>' % (self.symboles)


def from_base_10(number, to_base):
   """ Convert base 10 number to the given base

       Examples:

         Base 10 to hexa :

         >>> from_base_10(1000, "0123456789ABCDEF")
         '3E8'

   """
   return BaseConverter(to_base).from_base_10(number)


def to_base_10(string, from_base):
   """ Convert custom base string value to base 10

       Examples:

         Base hexa to 10 :

         >>> from_base_10('3E8', "0123456789ABCDEF")
         1000

   """
   return BaseConverter(from_base).to_base_10(string)


def switch_base(string, from_base, to_base):
   """ Convert custom base string value to another custom base

       Base should be a list of symboles.

       Examples:

         Hexa to binary :

         >>> switch_base('1A', "0123456789ABCDEF", "01")
         "11010"

   """
   base10 = BaseConverter(from_base).to_base_10(string)
   return BaseConverter(to_base).from_base_10(base10)
