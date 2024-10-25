# Parsing Inline Markdown

We need to figure out how to parse inline markdown.

There are some challenges associated with this because markdown can have nested inline styles.

Code can be nested in *styled* text, but text nodes in code styled nodes cannot be styled.

In that sense, if we encounter the code '`' delimiter, anything within it should only be considered code. The same can be said of images.

Considering this, if we intend to parse inline text in-sequence (or as we encounter it), how would we go about doing it?

`code` is treated specially. and ![images]() are treated specially.

For now I'm not going to worry about building a lexer or an official parser

That said, I think I have an ok idea

given some block of text:

I'm going *to **write `some` [stuff]()***

if we look at this character by character assuming that it is only a normal text block:
I, ', m,  , g, o, i, n, g,  , * (STOP)

we've seen a character that could denote either an italicized OR bolded block, we need to confirm which it is. Look ahead by one character:
t (STOP)

The next character does not equal '*' so we know that this MUST be an italicized block.

Whatever comes next, until we encounter another '*' should be in an italicized block:
t, o,  , * (STOP)

We have just encountered a character that denote either the end of this italicized block OR the start of a Bolded block. Look ahead by one characterl

if we split by code first: 

'I'm going *to **write ', 'some', ' [stuff]()***'

This will render, text.text(I'm going *to **write ), text.code(some), text.text( [stuff]()***)

if we then feed this back in splitting by bolded we should get:

'I'm going *to ', 'write ', 'some', ' [stuff]()', '', '*'

which gives us:
text.text('I'm going *to '), text.bold(write ), text.code(some), text.text( [stuff]()), text.bold(), text.text('*')

if we then feed this again for italicized we should get
t.t(I'm going ), t.i(to ), t.b(write ), t.c(some), t.t( [stuff]()), t.b(), t.i()

I'm wondering what this composes to with something simpler

***`code`***

split by '`'

t.t(***), t.c(code), t.t(***)

split by '**'

t.b(), t.t(*), t.c(code), t.b(), t.t(*)

split by '*'

t.b(), t.i(), t.c(code), t.b(), t.i()

if we pass this into our text_node_to_html what happens?
It works!

He's the problem though
If you pass something like '***' you'd get a bunch of empty html tags that do nothing

There could be a pass through the inline material to
