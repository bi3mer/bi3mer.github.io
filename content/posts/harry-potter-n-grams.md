+++
date = '2019-09-05T15:32:07-05:00'
draft = false
title = 'N-Grams With Harry Potter'
+++
I recently started grad school and one of the classes I am taking is Natural Language Processing (NLP). Before the class I decided to watch a few videos on NLP and came across N-Grams. I have not made it known in any of my past posts but I love N-Grams. One of my projects is around reinforcing N-Grams which I hope to post about sometime later this year. Digression aside, I decided it would be a fun project to write an n-gram that uses the text of Harry Potter as input and see what we get; I know it isn't the most original idea but it was fun.

Before we can get into the results, let's go over n-grams. The "n" in n-gram is meant to represent some integer greater than 0. The "gram" is short for grammar. When you put it together you get a grammar that takes an input of size `n` and returns the word that is likely to be next. Let's take a small example sentence to show the concept, "Colan was here yesterday and was here today." With this example let's construct a n-gram where `n` is equal to two.

To parse this sentence for a n-gram of size two, the first input is "Colan was" and the result is "here." Meaning when the grammar receives the phrase "Colan was" the grammar will expect the next word to be "here." So let's show what the grammar looks like at this phase.

```
{
  "Colan was": {
    "here": 1
  }
}
```

You'll notice that we have "here" correspond to the value of one. This is because we are currently parsing the input and keeping track of the number of occurrences. When we are done setting up our input we can compile the grammar into something that will predict the next output. But more on that after we are done counting the occurrences. The next set of input is "was here" with the result of "yesterday". Following that you will get "was yesterday" corresponding to "and." This will go on until we get the final result below.

```
{
  "Colan was": {
    "here": 1
  },
  "was here": {
  	"yesterday": 1,
  	"today": 1
  },
  "here yesterday": {
  	"and": 1
  },
  "yesterday and": {
  	"was": 1
  },
  "and was": {
  	"here": 1
  }
}
```

Now that we have created a grammar that counts all the occurrences we can compile it which means we can turn it into a set of probabilities. There are two ways to do this, weighted and unweighted. What I call the unweighted approach is one where the occurrences are ignored and each potential value is given the same weight. In this case we would take "was here" and automatically apply `0.5` to both values regardless of how many occurrences there actually were. The weighted approach is one where we do use the occurrences and calculate each value by dividing the values occurrences by the number of occurrences for the key. In our example, both the weighted and the unweighted versions are the same.

```
{
  "Colan was": {
    "here": 1
  },
  "was here": {
  	"yesterday": 0.5,
  	"today": 0.5
  },
  "here yesterday": {
  	"and": 1
  },
  "yesterday and": {
  	"was": 1
  },
  "and was": {
  	"here": 1
  }
}
```

With this compiled version we can now use this grammar to predict the next word and generate some interesting text. In our case we can use the input "Colan was." Looking at the compiled grammar we know the value given back is "here." However, if we continued it would then take "was here" and return either "today" or "yesterday" with both having a fifty percent chance. If we continued it would generate something like, "Colan was here yesterday and was here yesterday and was here yesterday and was here today." Notice that once we get to "today," it can no longer generate anything.

This example, while small, shows the strengths and weakness of n-grams. It is an incredible structure that can quickly mimic style and technique used in the input to produce interesting but similar results. The larger the n, the more sensible the output will be as well as the more similar it will be to the input. On the other hand, it is limited by its very strengths. Ultimately we want AI to generate new and interesting things which n-grams can inherently not do.

Now that we, hopefully, understand n-grams we can get to what happens when we apply n-grams of sizes one to six on the first two books of Harry Potter. If you would like to see my implementation of this you can see the [source on github](https://github.com/bi3mer/nlp_experiments/blob/master/naive_n_gram.py). I think you can see that the weighted versions of the grammar tend to read a bit more sensibly, especially when n is lower. You'll also notice that n-grams can have trouble with quotes, especially when they are long and use commonly found phrases.

## N=1
#### Unweighted Output
> for the first time in his body . hang glider on nettle wine’s left on “don’t — thing left.” he grunted into glowing in him norbert,” said “hello nick,” said uncertainly. “a boa constrictor’s tank and scared. “what really there is?” “i repeat if that’s it simply waved it out.” harry “because being one thought you speak about anything justin might think!” harry joined them weren’t nearly killed ’em. horribly. “yes exactly. i expect,” said “but they weren’t. he handed it also bring silence. the desk just managing to trundling around unseen.” harry loaded into any moment hedwig soared back out gryffindor ghost began to detect

#### Weighted Output
> for the first time in his muggle shop without ending with our own house!” harry watched the great glinting emeralds. harry remembered that ruddy stargazers. not say anything missing?” harry looked as he was always was on in front page were there stood there was disheveled. ignoring her put him what mcgonagall transfigured or tickled them inside. hermione remained of slytherin wished he threw him as paving stones bound to a soft voice. “and women,” wood and the diary. all that ter pay for the faintest sound. where the entrance hall. “just been sent me.” feeling about you must be those bits of books into applause

## N=2
#### Unweighted Output
> for the first time in his throat — i then screwed up his robes was what looked like bodyguards. “oh this doesn’t often happen at hogwarts — i only hope we can get something of the few owls that managed to beat away. mr. weasley passing harry and malfoy barely inclined their heads not taking his eyes as narrow as he handed uncle vernon came in harry. you found it inside one of our kind underwent so many students filed past the giant serpent uncoiling itself rapidly slithering out onto the platform?” she said sharply. “why?” “funny stuff on the mantelpiece. george groaned. “mum we know

#### Weighted Output
> for the first time in his tracks and harry were up in his hand. “i’ve got to go to hogwarts.” uncle vernon held it up there — ” “was that you?” said harry “but what’s curious?” mr. ollivander was flitting around the room was almost dark now but i got back from the dog was guarding the stone.” harry looked up at the end of a wizard’s duel?” said harry. nearly headless nick and madam pomfrey told me in the bedroom window and passed it out flicked it open and pulled his wand and turned to stare at the troll stopped next to the entrance hall.

## N=3
#### Unweighted Output
> for the first time in his life. he was hungry he’d missed five television programs he’d wanted to see me professor dippet?” said riddle. he looked nervous. “sit down,” said harry politely pointing at the topmost pane where around twenty spiders were scuttling apparently fighting to get through all their extra work. “i’ll never remember this,” ron burst out one afternoon throwing down his quill in a transport of rage. “i’ll have you this time i’ll have you!” and without a backward look. then dented scratched and steaming the car rumbled off into the night. “i shall see you soon i expect professor mcgonagall,” said hagrid.

#### Weighted Output
> for the first time in his life until a month ago and he told ron and hermione had brought out of the hall hermione hurrying alongside them. as they went upstairs to meet ron in the library with her trying to get near enough to hear what they were saying. their mother had just taken out her handkerchief. “ron you’ve got something on your nose.” the youngest boy tried to jerk out of the troll’s hand rose high high up into the giant face above it was ancient and monkeyish with a long white finger. “i’m sorry to say i sold the wand that did it,”

## N=4
#### Unweighted Output
> for the first time in his life harry was pleased to hear the note of panic in his voice. “yeh are if yeh want ter stay at hogwarts,” said hagrid fiercely. “yeh’ve done wrong an’ now yeh’ve got ter pay fer it.” “but this is servant stuff it’s not for students to do. i thought we’d be copying lines or something if my father knew i was doing this he’d — ” “ — is the golden snitch,” said harry “and it’s very small very fast and difficult to see. it’s the seeker’s job to catch it. you’ve got to weave in and out of focus.

#### Weighted Output
> for the first time in his life a high cold cruel laugh. hagrid was watching him sadly. “took yeh from the ruined house myself on dumbledore’s orders. brought yeh ter this lot ...” “load of old tosh,” said uncle vernon. harry jumped he had almost forgotten that the dursleys were there. uncle vernon certainly seemed to have changed her mind about snape. “i know a jinx when i see one hagrid i’ve read all about them.” ron dropped his wand. hermione granger telling a downright lie to a teacher “if they hadn’t found me i’d be dead now. harry stuck his wand up its nose and

## N=5
#### Unweighted Output
> for the first time in his life. his aunt and uncle hadn’t been able to think of anything else to do with him but before they’d left uncle vernon had taken harry aside. “i’m warning you,” he had said putting his large purple face right up close to harry’s “i’m warning you now boy — any funny business anything at all — and you’ll be in that cupboard from now until christmas.” i’m not going to do anything,” said harry “honestly but uncle vernon didn’t believe him. no one ever did. the problem was strange things often happened around harry and it was just no good

#### Weighted Output
> for the first time in his life. his aunt and uncle hadn’t been able to think of anything else to do with him but before they’d left uncle vernon had taken harry aside. “i’m warning you,” he had said putting his large purple face right up close to harry’s “i’m warning you now boy — any funny business anything at all — and you’ll be in that cupboard from now until christmas.” i’m not going to do anything,” said harry “honestly but uncle vernon didn’t believe him. no one ever did. the problem was strange things often happened around harry and it was just no good

## N=6
#### Unweighted Output
> for the first time in his life. the potters smiled and waved at harry and he stared hungrily back at them his hands pressed flat against the glass as though he was hoping to fall right through it and reach them. he had a powerful kind of ache inside him half joy half terrible sadness. how long he stood there he didn’t know. the reflections did not fade and he looked and looked until a distant noise brought him back to his senses. he couldn’t stay here he had to find his way back to bed. he tore his eyes away from his mother’s face whispered

#### Weighted Output
> for the first time in his life a high cold cruel laugh. hagrid was watching him sadly. “took yeh from the ruined house myself on dumbledore’s orders. brought yeh ter this lot ...” “load of old tosh,” said uncle vernon. harry jumped he had almost forgotten that the dursleys were there. uncle vernon certainly seemed to have got back his courage. he was glaring at hagrid and his fists were clenched. “now you listen here boy,” he snarled “i accept there’s something strange about you probably nothing a good beating wouldn’t have cured — and as for all this about your parents well they were weirdos

