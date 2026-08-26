# -*- coding: utf-8 -*-
"""Harvested Google reviews for Downtown Orthodontics.

Source: the practice's live Google Business Profile, read 26 August 2026.
Aggregate at time of harvest: 4.4 from 160 reviews.

EVERY review here is VERIFIED 5-star. Verification method, because Google's review
panel exposes no accessible rating markup at all (no aria-label, no title, no schema,
the stars are pure SVG): the panel was sorted by "Lowest rating" and the ordered author
list read off. In that order the transition to 5-star lands exactly at "S Ismail", so
the 28 authors listed before it are the complete non-5-star set for this profile:

    Barbara Chung · Amber Sekhon · Travel Note · James Riley · Tobi Akinbiyi ·
    Jennifer Stadnychuk · Lily Yve · Sara Elizabeth Gerrie · Anna Nesterchuk · Julia ·
    Kate Mckinon · abc100785 · chloe · jiatong shi · Dylan Boyce · Elizabeth Clark ·
    Dayton Cahill · Sue Zen · 陽子 · SL · Ryan · Mathieu Tessier · jun xu · Raven Li ·
    Atlas Hanen · ade ojengbede · Miu Leung · Jennifer Hershman

Atlas Hanen was a candidate and is 4-star, so it is EXCLUDED. Do not add it back.
Spot-checks on S Ismail, Dante Foreman, Zhenya Beck, Riaz Meghji, Fiona Deng,
kimia Nalchi, Vee L, sanaz hendi, Bonnie Hastings, Pinky, Roger Singh, Lindy Thomas
and Alex Bobylev were also confirmed visually against the rendered star rows.

TEXT RULE: verbatim. Long reviews are trimmed with a trailing ellipsis and never
reworded, per REVIEWS-SPEC rule 2. `job` records what claim each review proves, so
nobody pads the wall with generic praise later.
"""

RATING = "4.4"
COUNT = 160
HARVESTED = "26 August 2026"

# The Google profile link. This is the canonical cid URL, and it is the SAME one the
# homepage rating line already uses, so the two agree.
GOOGLE_URL = "https://www.google.com/maps?cid=9098292092356715373"

# (name, when, category chip, verbatim text, job it does)
SPOTLIGHT = (
    "Sally Karimi", "a year ago", "Complex case",
    "I came to Dr. Daher with a complex Class III orthodontic case. For years, I had been "
    "told by various professionals that jaw surgery was the only way to fix my bite and "
    "alignment issues. Needless to say, I was nervous, skeptical, and losing hope. But "
    "everything changed the moment I walked into his clinic&hellip; What truly amazed me was "
    "that Dr. Daher looked at my case and, with full confidence, said: &ldquo;This is completely "
    "doable with Invisalign, no surgery needed.&rdquo; His assurance gave me the confidence I "
    "needed, and I signed on that day, one of the best decisions I&rsquo;ve ever made&hellip; "
    "It&rsquo;s only been eight months, and although my treatment isn&rsquo;t even finished yet, "
    "the results are already absolutely incredible. I never imagined I&rsquo;d see this kind of "
    "transformation without surgery, and so quickly!",
    "The strongest proof on the whole profile for the conservative-treatment claim: told by "
    "others that surgery was the only option.",
)

REVIEWS = [
    ("Alex Bobylev", "10 months ago", "Specialist care",
     "Nearing the end of my Invisalign treatment with Dr. Sam Daher, my biggest regret is that "
     "I didn&rsquo;t come across his excellent clinic sooner. He is repairing the work I had done "
     "at a regular dentist and doing it quicker, better and with far less discomfort&hellip; It "
     "took 2 years longer than originally estimated, was highly uncomfortable, and in the end "
     "couldn&rsquo;t close some of the gaps and straighten out the upper front row.",
     "Specialist versus a general dentist doing aligners, which is the site's central wedge."),

    ("Lomish Bhangu", "4 months ago", "Complex case",
     "I came in with a very complex bite issue that left me unable to chew about 80% of foods. I "
     "was also in a lot of constant pain which was becoming unmanageable. I had previously been "
     "turned down by one orthodontist, and another wasn&rsquo;t able to provide a real solution. "
     "It was frustrating and discouraging, until I met Dr. Daher. Dr. Daher gave me hope when I "
     "really needed it&hellip; I would highly recommend Downtown Orthodontics to anyone, "
     "especially those with more complex cases.",
     "Complex and referred cases welcome."),

    ("S Ismail", "5 months ago", "First visit",
     "Dr. Sam Daher is extremely professional and knowledgeable. He takes the time to walk you "
     "through the treatment plan, answers questions thoroughly, and makes you feel confident in "
     "the process. You can tell he has a lot of experience, and that reassurance makes a huge "
     "difference.",
     "The consultation actually explains the plan."),

    ("Kim Patara", "8 months ago", "Retention",
     "Very friendly reception staff! Hygienist was quick, professional and friendly! Dr. Daher is "
     "very personable and professional! He did my original Invisalign in 2007 and teeth have not "
     "shifted.",
     "Results hold: an eighteen-year-old case still straight."),

    ("Riaz Meghji", "4 months ago", "Worth it",
     "Dr. Daher and his team were fantastic. Their attention to detail and extra care helped "
     "deliver an outstanding result that was well worth the investment. Highly recommend!",
     "Answers the price objection from the patient's side."),

    ("Vee L", "a year ago", "Never rushed",
     "Dr. Daher has been amazing throughout my Invisalign treatment plan! There was a few "
     "ownership changes but when Dr. Daher purchased the practice back it was as if he "
     "hadn&rsquo;t left, quickly jumped back in and completed my treatment plan. He was even "
     "generous to reopen my case as the previous orthodontist debonded everything when there "
     "were still gaps. My treatment plan took longer than the estimated time but I&rsquo;ve "
     "never felt rushed or pressured to finish my treatment quicker.",
     "Finishes the case properly rather than to a schedule."),

    ("Luna Cavasso", "9 months ago", "Redo work",
     "I came here to correct my bite after the permanent retainer installed by a previous "
     "(different) orthodontist broke&hellip; Dr Daher is very attentive and has done a great job "
     "of making adjustments along the way to make sure my bite turns out perfect. Appointments "
     "also run very efficiently; aside from the initial one, I don&rsquo;t think any appointment "
     "has run more than 20 minutes and I barely spend any time in the waiting area.",
     "Fixing another practice's work, and respecting a downtown professional's time."),

    ("SassySips", "a year ago", "Retainers",
     "I needed a new pair of Invisalign retainers and got an appointment the same day I called. "
     "Beautiful office, super clean and quick appointment from booking to getting out all within "
     "a few hours. Highly recommend if you need new retainers.",
     "Same-day retainer replacement, which is a real service line."),

    ("Fiona Deng", "5 months ago", "Kids",
     "Dr. Daher is a great orthodontist that you can trust! Both of my kids like him a lot!",
     "Children are comfortable with him."),

    ("Bonnie Hastings", "9 months ago", "Kids",
     "The team at Downtown Orthodontics is incredible, so professional and welcoming! They make "
     "every visit easy and comfortable. I trust them completely with my dental care and my "
     "kids&rsquo; future braces.",
     "A parent trusting the practice with the next stage."),

    ("Lindy Thomas", "2 years ago", "Kids",
     "I have been bringing my daughter to this practice for around three years to have her teeth "
     "straightened because they needed all lot of work&hellip; Dr. Daher (as well as his staff) "
     "took the time to talk to us and answered any and all of the questions or concerns we had. "
     "This is what I was hoping for! We are extremely happy with the results and the care that we "
     "have received.",
     "A full multi-year child case, start to finish."),

    ("Elizabeth May", "10 months ago", "Kids",
     "I brought my niece to Downtown Orthodontics and couldn&rsquo;t be happier with the "
     "experience. From the first consultation to the follow-up appointments, the entire team was "
     "professional, kind, and incredibly supportive. The staff made my niece feel comfortable and "
     "at ease, and they explained every step of the process clearly, both to her and to me.",
     "Explains treatment to the child as well as the adult."),

    ("Yasmin b Parsad", "5 months ago", "Kids",
     "We came to see dr Daher for my daughter teeth. Both him and his staff are wonderful, very "
     "helpful, very knowledgeable. We have been very happy with their services and definitely "
     "recommend them.",
     "Parent of a treated child."),

    ("Dante Foreman", "4 months ago", "First visit",
     "I got a scan here and I was in and out pretty quick. I got all of the information I need "
     "sent over to me very quickly, and while I was in there everyone was very friendly and "
     "helpful. Overall professional and nice facility.",
     "The free first scan, and what you leave with."),

    ("kimia Nalchi", "a year ago", "Invisalign",
     "Phenomenal service doesn&rsquo;t even begin to describe my experience. From the moment I "
     "walked in, Bita&rsquo;s professionalism and warmth stood out, she&rsquo;s the main reason I "
     "decided to start my Invisalign journey here. Dr. Dahar is equally incredible, kind, deeply "
     "knowledgeable, and makes you feel completely at ease. I just received my Invisalign today "
     "and the entire process was seamless, quick, and genuinely enjoyable.",
     "Starting Invisalign, and the team by name."),

    ("Roger Singh", "9 months ago", "Retention",
     "If your thinking about having Invisalign, Dr. Daher is the orthodontist you want to consult "
     "with. His warm and friendly disposition makes you feel like a family member and not just "
     "another patient or file #. I had the Invisalign treatment preformed by him about 13 years "
     "ago however, return every 4 years to reorder the Invisalign retainers.",
     "Thirteen years on and still a patient."),

    ("Sehar Lalani", "2 years ago", "Invisalign",
     "Would highly recommend their services! Dr Sam Daher and his team are amazing, I&rsquo;m so "
     "glad I chose to get my Invisalign treatment done with them. Everyone is really pleasant, "
     "the team is super responsive over email/phone, and they always make time to make you feel "
     "welcome. I&rsquo;m so grateful to Dr Daher for resuming my treatment despite the pandemic "
     "interrupting things&hellip; He genuinely cares and is always a pleasure to speak with!",
     "Picked treatment back up rather than dropping the patient."),

    ("Jayden Dinh", "6 months ago", "The visits",
     "I had the best experience ever with Dr. Daher and I couldn&rsquo;t be happier with my "
     "results. Dr. Daher and his team are friendly and professional. I always looked forward to "
     "going to my ortho appointments (which is crazy!). Thank you so much for everything.",
     "Finished treatment, and actually enjoyed the visits."),

    ("Chlo&euml; McCarron", "5 months ago", "Invisalign",
     "Downtown Orthodontics team is very welcoming, starting from the very first visit with Bita. "
     "I was ready &amp; excited for treatment and they got me started right away. The team is all "
     "friendly. For such an important heath decision, I am confident with my Orthodontist Dr. "
     "Daher guiding my Invisalign treatment.",
     "No waiting to start, and confidence in the specialist."),

    ("Mary Remoue", "5 months ago", "Results",
     "I have found the entire team to be caring, compassionate and extremely good at what they "
     "do. From the moment I walked into the beautiful, clean and very organized office, I have "
     "had nothing but a great experience. The progress of my teeth has been quick and perfect, "
     "thanks to Dr. Daher and his fabulous team!",
     "Progress mid-treatment."),

    ("Sajda Zubedi", "2 years ago", "First visit",
     "Dr. Daher and the staff are not only highly skilled but also incredibly friendly and "
     "accommodating. They took the time to explain every step of the process, ensuring I was "
     "comfortable and informed throughout my appointment. The clinic itself is modern, clean&hellip;",
     "Informed consent done properly."),

    ("sanaz hendi", "2 years ago", "First visit",
     "I recently had the pleasure of visiting Downtown Orthodontics, and my experience was "
     "exceptional. The office is clean, modern and well designed. The staff is super friendly and "
     "helpful. The orthodontics professionals thoroughly assessed my needs and explained the "
     "treatment plan in a way that was easy to understand.",
     "A thorough assessment, explained plainly."),

    ("JJ", "a year ago", "Braces off",
     "Dr Sam Daher and his assistant are always punctual and professional, know their patients, "
     "and him and his assistant are nothing short of fantastic!! Dr Sam Daher and his assistant "
     "made me feel very comfortable. My braces came off today it was a big day for me. I had my "
     "retainers put on and Dr Sam Daher&rsquo;s assistant took the time to show me how to put "
     "them on and take them off.",
     "A finished braces case, and the retention handoff."),

    ("Allen Alvarez", "a year ago", "Invisalign",
     "Michaela gave me such a warm welcome to Downtown Orthodontics after I finally followed my "
     "dentist referral. She explained what they offered which helped me make the decision about "
     "Invisalign.",
     "A dentist referral converting into treatment."),

    ("Zhenya Beck", "3 months ago", "The doctor",
     "Love these people! Dr. Daher is a wonderful human being, very knowledgeable, skillful and "
     "empathetic professional. Highly recommended.",
     "Skill and empathy together."),

    ("amber rold", "4 months ago", "Invisalign",
     "Absolutely fantastic staff, kind and accommodating. My teeth look great! Would absolutely "
     "recommend for invisalign treatment.",
     "A finished Invisalign result."),

    ("Pinky", "6 months ago", "The doctor",
     "Dr. Daher is amazing! So helpful, kind and understanding. He is so supportive and very "
     "skilled at what he does. I highly recommend him.",
     "Short, warm, and about the doctor rather than the office."),
]

# Chips are Google's OWN review topics with Google's own counts, read from the profile on
# 26 August 2026. Not our invention, and not editable without re-reading the profile.
GOOGLE_TOPICS = [
    ("friendly team", 12), ("clean environment", 7), ("invisalign", 5),
    ("attentive doctor", 4), ("experienced orthodontist", 3), ("clean clinic", 3),
    ("clear treatment plan", 2), ("friendly dentists", 2), ("affordability", 2),
    ("organized staff", 2),
]
