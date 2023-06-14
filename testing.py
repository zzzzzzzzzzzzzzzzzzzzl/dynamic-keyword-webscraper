from scripts.outputData import *
from scripts.functions import *


data = [
    {
        "textsWithKeyWords": {
            "text": [
                "In the midst of our conversion into the digital era, we sometimes find ourselves on the edge of the fence, gazing over the paddocks trying to determine which grass is greener. The digital era ..."
            ],
            "keywords": ["green"],
        },
        "page": "https://www.burgerfuel.com/nz",
    },
    {
        "textsWithKeyWords": {
            "text": [
                "In the midst of our conversion into the digital era, we sometimes find ourselves on the edge of the fence, gazing over the paddocks trying to determine which grass is greener. The digital era ..."
            ],
            "keywords": ["green"],
        },
        "page": "https://www.burgerfuel.com#mm-2",
    },
    {
        "textsWithKeyWords": {
            "text": [
                "You are an organic machine, a sensational human and your engine deserves the most pure, natural ingredients, ripped straight from mother natures sweet bosom before anyone's had the chance to defile them. Our super natural gourmet burgers are made to be eaten with pure, unadulterated, unbridled passion (there's no time for knives and forks here... but we're always down for a spoon, if you're offering) and every mouthful should be a celebration of the most beautiful things in life, like pure fuel and your bad assery.",
                "You are an organic machine, a sensational human and your engine deserves the most pure, natural ingredients, ripped straight from mother natures sweet bosom before anyone's had the chance to defile them. Our super natural gourmet burgers are made to be eaten with pure, unadulterated, unbridled passion (there's no time for knives and forks here... but we're always down for a spoon, if you're offering) and every mouthful should be a celebration of the most beautiful things in life, like pure fuel and your bad assery.",
            ],
            "keywords": ["natural", "organic"],
        },
        "page": "https://www.burgerfuel.com/nz/our-food/fuel-for-the-human-engine",
    },
    {
        "textsWithKeyWords": {
            "text": [
                "You deserve nothing less than the best. That's why we leave no stone unturned in our relentless quest for the freshest, most pure, natural ingredients we can get our hands on. It's also why we make sure that your meal is made to order, when you order, and prepared with the utmost care, preparation, and burger making respect.",
                "Our chicken is the real deal - we never use fillers and it must be ethically raised. That's why we serve only 100% free range natural chicken breast - and say no to processing, hormones, additives, and GMO's.",
                "Fresh natural aioli. Just another taste. Just another hit. Addiction made daily. \u200b",
                "Fresh natural aioli. Just another taste. Just another hit. Addiction made daily. \u200b",
                "Batch brewed tomato relish, naturally aged so the acid drops and the sweetness hops.",
                "Batch brewed tomato relish, naturally aged so the acid drops and the sweetness hops.",
                "Our sweet, tomato relish is crafted using whole fresh fruit and vegetables, selected herbs and natural spices. Naturally sweet and aged to perfection.",
            ],
            "keywords": ["natural"],
        },
        "page": "https://www.burgerfuel.com/nz/our-food/pure-ingredients",
    },
    {
        "textsWithKeyWords": {
            "text": ["All-natural BurgerFuel Thickshakes made fresh to order."],
            "keywords": ["natural"],
        },
        "page": "https://www.burgerfuel.com/nz/our-food/burgers",
    },
    {
        "textsWithKeyWords": {
            "text": [
                "Cheeseburger, spud fries with fresh natural free range BurgerFuel Aioli or tomato sauce and a small juice",
                "Milk thickshakes made with all-natural BurgerFuel Whip",
                "Soy thickshakes made with all-natural BurgerFuel Whip",
            ],
            "keywords": ["natural"],
        },
        "page": "https://www.burgerfuel.com/nz/order",
    },
]

arr = removeDuplicateFromTextWithKeyWords(data)


fileManager("testing.json", arr).save()
# outputData(data, "abcdefg")
