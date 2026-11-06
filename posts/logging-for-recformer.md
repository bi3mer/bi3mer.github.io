+++
date = '2025-03-27T00:15:32-04:00'
draft = false 
title = 'Logging for Recformer'
+++

One of my regrets is not actively writing about [*Recformer*](https://bi3mer.github.io/recformer/)[^github] as I implemented it. I realized this while writing my [last blog post](/posts/astar-for-recformer/), and this post is me trying to rectify that mistake. So, in this post I am going to discuss logging for *Recformer*. 

## Why Does *Recformer* Need Logging?

Great question! *Recformer* is part of the work I'm doing for my dissertation. The work I have done up and to this point has shown that the [method I created for dynamic difficulty adjustment via procedural level assembly](https://arxiv.org/pdf/2304.13922) works when tested with agents, but I have not shown that it has any effect when player's (i.e., actual human beings) interact with it. To address this, I am running several studies with real player's to see how the system works. And while I will be asking the user to fill out a survey to learn more about the player's experience, I also want quantitative data (e.g, levels completed, time played, etc.), and this is why *Recformer* needs logging.

## Logging Requirements

The first thing to consider is not what will be logged, but how will we get the logs? The approach with the least amount of work is to create a log file during gameplay and have participants email us the resulting file. This, though, is a bad approach because there is no guarantee that the participant will go through the extra steps to email the log file. The better approach is to log files to a server and then pull from the server.[^recformerhosting]

There are a lot of approaches available to make this work, and the right choice depends on the use case. The use case for *Recformer* is a very simple one. At a maximum, I expect there to be 200 concurrent users, but it will likely be much less. As a result, it doesn't really matter whether I roll my own server or use a provider like [AWS](https://aws.amazon.com/) or [GCP](https://cloud.google.com/). What does matter is (1) convenience and (2) price. Coding up my own logging service and then self-hosting or hosting on a cloud platform is both inconvenient and not inherently cheap. The cheapest option is going to be one that is free, and major cloud platforms like AWS and GCP provide exactly that. The choice of one or the other is pretty much arbitrary for the use case. As a result, I went with GCP because I wanted to test sending logs to [FireBase.](https://firebase.google.com/)

The database that FireBase gives its users access to is structured as collections of [JSON](https://www.json.org/json-en.html) documents. You can send documents to a collection with its [SDK.](https://firebase.google.com/docs/reference/node) 

So, what should be logged? The first thing we need is a way to differentiate users. Every player will be assigned a [random UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier#:~:text=A%20Universally%20Unique%20Identifier%20) when they open the webpage. Getting a UUID on a browser is easy. You can use: `crypto.randomUUID()`. With this, we have our first field in our logs. 

```json
{
    "id": "4498acce-abbf-4934-bb01-135217f42247"
}
```

An `id` is all well and good, but we need more if we want to learn anything about the player's experience while playing *Recformer*. For example:

- How many levels did the player play? 
- How many levels did the player beat? 
- Which level did they beat?
- How long did the player play?
- In what ways did the player lose?
- etc.

These kind of questions determine the kinds of logs that we should be trying to produce. In our case, I'm going to break our logs (i.e., documents) down into one document per level played by the player. So, what do we need for every level before a log is made and sent to the server? 

```js
    "id": UUID,
    "version": string,
    "condition": string,
    "result": "won" | "fell" | "ENEMY",
    "coins-collected": int,
    "time-played": float,
    "levels": [string],
    "order": int,
    "pathX": [float],
    "pathY": [float],
    "velX": [float],
    "velY": [float],
```

- "id" will only be assigned to a random UUID in the version used in the player study.
- "version" is the version of the game (i.e., 1.0.0).
- "condition" tells us which condition the participant was randomly assigned.[^condition]
- "result" tells us the overall result, which is either the player won or the way that they lost. The "ENEMY" value refers to the entity type (i.e., horizontal enemy, vertical enemy, etc.) that the player ran into, which caused them to lose.
- "levels" is an array of ids. If you read [the last post,](../astar-for-recformer/) then you may recall the use of `idToLevel`, which is dictionary where a string id maps to a level segment. These ids are what will populate the array, and they are used to form a level by concatenating smaller level segments together.
- "order" is an incrementing integer which starts at 0. The second level a player plays will have a log with order set to 1, and so on. This lets us order a players playthrough to better understand how much progress they made. 
- Finally, "pathX", "pathY", "velX", and "velY" give us the player's position and velocity. This isn't something that I am particularly interested in but is relevant for another study that will use *Recformer*. 

## Tracking Data

Tracking the data to get the log from above is fairly simple. The player's `id` is assigned once and then we reuse it for the rest of gameplay. The same is true for `condition`. Things are bit more complicated with `time`, where we have to track when the player started the level and when they finished. When they finish, we can also mark what the result was, which includes the number of coins collected and levels played. (We can also increment order.) Where things are less clear, though, is when we talk about the player's position and velocity.

*Recformer* is a browser game, and that means it draws to a canvas and uses [`window.requestAnimationFrame(...)`](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) to loop. Depending on the refresh rate of the player's display, the game may be 30fps, 60fps, 140fps, or anything else. So, even if we wanted to be lazy and log the player's position and velocity every frame, we know that the decision would be a bad one because our analysis would have to either figure out the refresh rate of the player's screen or not care. Further, I don't want, for example, 140*4 floats, for every second of gameplay.

The solution that I'm going to go with is to store the data every tenth of a second, which means 40 floats stored per second of gameplay, but, just as a reminder, we won't be sending these in real-time. Instead, data will only be sent after the player has finished playing a level.

## Storing Data in Firebase

The first thing to do is to make a FireBase project in GCP's console, and then add a [FireStore](https://firebase.google.com/docs/firestore) database. This is where we'll send our logs. Then, go to to project settings (gear icon towards the top left) and add a web app. When you fill in a name, such as "My Web App", you'll be shown some code to access the database.

```js
const firebaseConfig = {
  apiKey: "xxxxxxxxx",
  authDomain: "xxxxxxxxx",
  projectId:"xxxxxxxxx",
  storageBucket: "xxxxxxxxx",
  messagingSenderId: "xxxxxxxxx",
  appId: "xxxxxxxxx"
};
```

As a general rule, you should not expose the config above for the many obvious security concerns. However, this is where running a player study has some advantages. Mainly, our webpage will be exposed to the public only while the player study is running. So, we can risk being insecure and lazy. It still isn't great practice because a scraper will probably catch the config, but once we have the data, there is nothing stopping us from deleting the project and making said configuration useless.

Alright, so now that we have their code set up. Sending data to the database is easy:

```js
import { initializeApp } from "firebase/app";
import {
  addDoc,
  collection,
  Firestore,
  getFirestore,
} from "firebase/firestore";

const app = initializeApp(firebaseConfig); // fake config above
const db = getFirestore(app);

const submission = {
    // data goes here
};

addDoc(
    collection(db, `[[COLLECTION NAME HERE]]`),
    submission,
);
```

Now we can send data to the database, let's talk first about sending the right data, and then we'll talk about pulling the data down for analysis.


### Submitting the Right Data

Most of the analytics we decided on our pretty easy. Did the player win? We know that when the level is over. If the player died, we also only know this when the level is over. When that occurs, though, we don't necessarily want to make a call to the database through the player game object or something else that wouldn't make sense. Instead, we'll use a [static class](https://www.w3schools.com/jsref/jsref_class_static.asp) where we can write data to. Then, we'll put the logic for writing to the database in the game scene.

The only tricky data type to store is the player's position and velocity. The original solution I came up with was to create a game object and add it to the game model which uses `dt` to keep track of time. However, here is one of the problems with implementing everything from scratch: my engine does not support game objects without physics. So, I could add a game object anyways, but then physics calculations would be run every frame for it. Sure, I'd make it so gravity wouldn't effect the object, but it felt wrong to me. So, instead, I put the timer in the game scene as a separate object.

```js
export class RepeatingTimer {
  private startTime: number;

  constructor(
    private runTime: number,
    private callback: () => void,
  ) {
    this.startTime = 0;
  }

  public update(dt: number) {
    this.startTime += dt;
    if (this.runTime <= this.startTime) {
      this.startTime = 0;
      this.callback();
    }
  }
}
```

Then, I put an instance of `RepeatingTimer` in the game scene.

```js
onEnter(): void {
    ...
    this.timer = new RepeatingTimer(0.1, () => {
        const player = this.game.dynamicEntities[0];
        Logger.pushPlayerPositionAndVelocity(player.pos, player.velocity);
    });
}

update(dt: number): void {
    this.game.update(dt);
    this.timer.update(dt);
}
```

If you are curious, there is a point at which I would decide to add support for non-physics objects in the game, and that point would be when I have one more relevant use case. But, I don't have any such use case so I won't be adding that support to *Recformer*'s engine, at least not yet.

### Getting the Data From FireStore

There is no point storing data if we can't use it. So, how do we get data from FireStore? The answer partly depends on the size of the data we're talking about. For our use case, we are talking about such a small amount of data that any cloud-based processing is overkill. Therefore, it is better and easier to pull the data down and do the analysis locally. We can accomplish this with [node-firestore-import-export](https://www.npmjs.com/package/node-firestore-import-export). 

```bash
npx -p node-firestore-import-export firestore-export -a firestore-key.json -b backup.json
```

To get the `firestore-key`, follow the directions below:

- Go to Firebase console
- Select the project
- Go to *project settings* (it's the gear icon at the top left)
- Go to *service accounts*
- Press *generate new private key*

After that, you can get a json file called `backups.json`—you can also rename it to whatever you want—which contains every collection and document in the FireStore database.

## Conclusion

I hope this helped. As per usual, feel free to reach out if you have any questions/comments/concerns/etc., and I hope you have a great day!

[^github]: All the code for *Recformer* is available on [GitHub](https://github.com/bi3mer/recformer).

[^recformerhosting]: *Recformer* is hosted on [GitHub Pages](https://pages.github.com/), which is completely free and allows you to host [static websites](https://en.wikipedia.org/wiki/Static_web_page)---meaning that you do not have a back and forth between the website and the host of said website.

[^condition]: It is redundant to store the condition that the player was assigned to for every level. A more space-efficient implementation would be to have a collection of documents that maps players to their assigned condition. 