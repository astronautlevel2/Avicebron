#!/usr/bin/env/python3

from discord.ext import commands


class Memes(commands.cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def t3ch(self, ctx, *, arg="server, sss, weeb, shack mod, trap role, channel, shitposting, cancerous"):
        """
        Prints the T3CHNOLOGIC copypasta.
        With no or missing arguments, defaults to the original pasta (or a modified original).
        Usage: [p]t3ch [server], [sss], [weeb], [shack mod], [trap role], [channel], [shitposting], [cancerous]
        """
        original = ["server", "sss", "weeb", "shack mod", "trap role", "channel", "shitposting", "cancerous"]
        replacements = [i.lstrip().rstrip() for i in arg.split(",")]
        del replacements[len(original):]
        if len(replacements) < 8:
            replacements = replacements + original[len(replacements):]

        await ctx.send(
            await commands.clean_content(
            ).convert(ctx,
                      ("y'know, i was trying to keep my cool and be a part of this {0}, but i cant force myself here any longer. "
                       "this isnt {1}. too much {2} shit, owned by a {3} and a former {3}, no {4}, "
                       "a {5} where people get warned for {6} when part of the spirit of {1} is {6}, "
                       "and overall just more {7} than {1} was ever meant to be. goodbye."
                       ).format(*replacements)))

    @commands.command()
    async def lenny(self, ctx):
        """Print lenny face ( ͡° ͜ʖ ͡°)"""
        await ctx.send("( ͡° ͜ʖ ͡°)")

    @commands.command()
    async def xk2(self, ctx):
        """
        Prints the *new* and *improved* xkyup copypasta from the Foxverse drama.

        Usage: [p]xk2
        """
        await ctx.send(
            await commands.clean_content(
            ).convert(ctx,
                      ("Hello there @everyone, Hello there, this is my apology I guess, I'm sorry for acting quite vigorously in the drama post "
                       "screenshots that astronautlevel made in which I said \"suck a dick\" if it wasn't obvious I was stressed out, I know nobody "
                       "will listen to me now but PokeAcer is a good dude with good intents no he isn't going to steal your password and decrypt "
                       "it in 1000 years, bcrypt is already salted and about bcrypted client side we are working on this."
                       )))

    @commands.cooldown(rate=3, per=10.0, type=commands.BucketType.channel)
    @commands.command(aliases=['xk'])
    async def xkyup(self, ctx, *, variant=""):
        """
        Prints the xkyup copypasta. Delimit arguments with ',' or pick one of the already defined variants.
        Possible variants: fr, es, it, jp, de, pl, pt, nl, se, bees, srb
        Usage: [p]{xkyup|xk} [variant]
            where variant can also be of the form [are transgender, transgender person, transgender, Aurora, trans commmunity]
        """
        xkyup = {
            "fr":
                ("Je suis tellement désolé, j'étais un putain d'attardé pour avoir dit des mots qui me mettraient dans le pétrin et qui mettraient beaucoup "
                 "de personnes qui sont transgenres ou qui sont en couple avec une personne transgenre. Je n'ai pas réfléchi avant d'avoir dit un mot donc "
                 "c'est juste sorti comme quelque chose de totalement faux, je ne déteste aucune personne transgenre, seulement la communauté. "
                 "J'aime bien Aurora, juste pas la communauté trans. Je suis désolé pour tout ceci. Tout ce que je demande c'est des excuses, "
                 "c'est tout. J'aurais du réfléchir avant de parler."
                 ),
            "es":
                ("Estoy muy arrepentido, fui un estupido retardado por decir esas palabras que me pondrian en problemas y hacer enojar a mucha gente que "
                 "son transexuales o que estan saliendo con una persona transexual. No pense antes de decir una palabra asi que salio como algo totalmente "
                 "mal. Yo no odio cualquiera que sea transexual,solo la comunidad. Me gusta Aurora, solo no la trans comunidad. Estoy arrepentido por todo "
                 "esto. Lo unico que pido es una disculpa. Tuve que haer pensado antes de hablar."
                 ),
            "it":
                ("Mi dispiace così tanto, sono stato un fottuto idiota per aver detto cose che mi avrebbero messo nei guai e avrebbero fatto arrabbiare un "
                 "sacco di persone che sono transgender o che stanno insieme ad una persona transgender. Non ho pensato prima di aprire bocca quindi è "
                 "sembrato qualcosa di completamente sbagliato, non odio nessuno che sia transgender, solo la comunità. Mi piace Aurora, solo non la "
                 "comunità trans. Mi dispiace per tutto questo. Tutto ciò che sto chiedendo è di chiedere scusa, tutto qui. Avrei dovuto pensare prima di parlare."
                 ),
            "jp":
                ("本当に申し訳ない, 私は多くのトランス人やトランス人をデートする人を怒らせる言葉で困ってしまった言葉を言ってからクソなリタードだった。 言葉を言った前に思ったなか "
                 "ったから全く間違っていた何かを来た、誰でもトランスジェンダは嫌いじゃなくてあのコミュニティだけ嫌い。オーロラが好き、トランスのコミュニティだけではない。これは本 "
                 "当にすみません。私が求めているのは謝罪だけ。話す前に思っていたはずだった。"
                 ),
            "de":
                ("Es tut mir sehr Leid, ich war ein verfickter Behinderter als ich diese Worte sagte und wusste nicht wie sehr ich Ärger kriegen würde und "
                 "wie sehr ich transsexuelle Menschen oder Menschen die transsexuelle daten erzörnen würde. Ich habe nicht gedacht bevor ich das Wort sagte "
                 "und so kam es raus als was komplett falsches. Ich hasse keine Transsexuellen, nur die Gemeinschaft. Ich mag Transsexuelle, nur nicht die "
                 "Gemeinschaft. Es tut mir sehr leid für all das. Ich bitte nur um Verzeihung. Ich hätte nachdenken sollen bevor ich den Mund aufgemacht habe."
                 ),
            "pl":
                ("Bardzo mi przykro, byłem jebanym idiotą gdy wypowiedziałem te słowa i nie zdawałem sobie sprawy z tego jak bardzo naprzykrze sie osobom "
                 "transseksualnym lub tym którzy chodzą z transseksualistami. Nie myślałem gdy wypowiedziałem te słowa i to co wyszło z moich ust było "
                 "smutne i nieprawidłowe. Nic nie mam do osób trans, tylko do ich społeczności. Lubie osoby trans, nie lubie tylko ich społeczności. Bardzo "
                 "mi za to wszystko przykro. Proszę o przebaczenie. Powinienem był pomyśleć zanim cokolwiek napisałem."
                 ),
            "pt":
                ("Peço imensa desculpa. Fui um grande retardado por dizer palavras que me iam meter em sarilhos com pessoas "
                 "trans ou que estão a namorar com uma pessoa trans. Eu não pensei antes de falar por isso aquilo saiu como algo totalmente mau, "
                 "eu não detesto ninguem que seja trans, só a comunidade trans. Eu gosto da Aurora, só não gosto da comunidade trans. "
                 "Peço desculpa por tudo isto. Só peço que me desculpem. Devia ter pensado antes de ter falado."
                 ),
            "be":
                ("Het spijt me zo erg, ik was een echt achterlijk om woorden te zeggen die mij in moeite zou brengen en die veel mensen "
                 "die transgender zijn of die in een relatie zijn met een transgender persoon boos zou maken. Ik heb niet nagedacht voor het "
                 "spreken, dus kwam het als iets totaal vals, ik haat niemand die transgender is, alleen de gemeenschap. Ik hou van Aurora, "
                 "alleen niet van de trans gemeenschap. Het spijt me voor dit alles. Alles what ik vraag is excuses, dat is alles. "
                 "Ik had moeten denken voordat ik sprak."
                 ),
            "nl":
                ("Het spijt me. Ik was gestoord omdat ik woorden zei die me in problemen zouden brengen en veel mensen boos maken die "
                 "transgender zijn of een transgender daten. Ik dacht niet na voordat ik iets zei, dus kwam het eruit als iets compleet "
                 "anders, ik haat niemand die transgender is, alleen de community. Ik vind Aurora aardig, maar niet de trans community. "
                 "Het spijt me heel erg. Alles waar ik voor vraag is een excuus. Ik had moeten nadenken voordat ik iets zei."
                 ),
            "se":
                ("hello guys im very sorry for punching a woman in discord chat. i do not understand what i do i am only muslim man "
                 "coming to sweden from long country away i am very sorry this has been very sad and i only want apology so i "
                 "do not bring shame on family that come sweden"
                 ),
            "bees":
                ("I'm so sorry, I was a fucking retard for saying words that would get me in touble and anger lots of people who are bees "
                 "or who are dating a bee. I didn't think before I spoke a word so it just came out as something totally wrong, I don't "
                 "hate anybody who is a bee, just the hive. I like bees, just not the beehive. I'm sorry for all of this. All I'm asking "
                 "for is a apology is all. I should have been thinking before I spoke."
                 ),
            "srb":
                ("Toliko mi je žao, bejah jebeni retard tako što izgovorih stvari zbog kojih ću izbući deblji kraj načiniti mnoge ljutim "
                 "koji su, ili koji su u vezi sa trans ljudima. Nisam mislio pre no što sam prozborio reč i ispalo je totalno pogrešno, ne "
                 "mrzim nikoga ko je trans, samo celokupnu zajednicu. Sviða mi se Aurora, samo ne trans zajednica. "
                 "Sve što tražim je izvinjenje. Trebao sam razmisliti pre no što bilo šta rekoh."
                 )
        }
        try:
            await ctx.send(xkyup[variant])
        except KeyError:
            original = ["are transgender", "transgender person", "transgender", "Aurora", "trans"]
            replacements = [i.rstrip().lstrip() for i in variant.split(',')]
            del replacements[len(original):]
            if len(replacements) < len(original):
                replacements = replacements + original[len(replacements):]

            await ctx.send(

                await commands.clean_content(
                ).convert(ctx,
                          ("I'm so sorry, I was a fucking retard for saying words that would get me in touble and anger lots of people who {} or who are dating {}. "
                           "I didn't think before I spoke a word so it just came out as something totally wrong, I don't hate anybody who is {}, just the community. "
                           "I like {}, just not the {} community. I'm sorry for all of this. All I'm asking for is a apology is all. I should have been thinking "
                           "before I spoke"
                           ).format(*replacements)))

    @commands.command()
    async def headpat(self, ctx):
        """Send someone a headpat"""
        await ctx.send("http://i.imgur.com/7V6gIIW.jpg")

    @commands.command()
    async def blackalabi(self, ctx):
        """Much regret"""
        await ctx.send("http://i.imgur.com/JzFem4y.png")
        
    @commands.command()
    async def rip(self, ctx):
        """F"""
        msg = await ctx.send("Press F to pay respects.")
        await msg.add_reaction("🇫")

    @commands.command(aliases=['bt'])
    async def blackalabitelegram(self, ctx):
        """Much regret telegram edition"""
        await ctx.send("https://imgur.com/t2FoObO")


def setup(bot):
    bot.add_cog(Memes(bot))
