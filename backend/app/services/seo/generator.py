"""Amazon Merch SEO listing generator - Design-focused, TOS compliant."""
import re
import random
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class SEOGenerator:
    """Generate TOS-compliant, design-focused listings for Amazon Merch."""

    # Words forbidden in Amazon Merch listings
    FORBIDDEN_WORDS = [
        # Product type words (NEVER use)
        "shirt", "t-shirt", "tshirt", "tee", "hoodie", "sweatshirt",
        "tank top", "tanktop", "long sleeve", "clothing", "apparel",
        "pullover", "crewneck", "raglan", "jersey", "top", "wear",

        # Fit/product descriptions (NEVER use)
        "lightweight", "classic fit", "slim fit", "relaxed fit",
        "cotton", "polyester", "fabric", "material", "sleeve",
        "double-needle", "hem", "stitched", "printed", "ink",

        # Amazon policy violations
        "best seller", "bestseller", "#1", "number one", "top rated",
        "amazon", "prime", "alexa", "kindle", "echo", "aws",
        "authentic", "genuine", "official", "licensed", "trademarked",
        "free shipping", "discount", "sale", "cheap", "affordable",
        "limited edition", "exclusive", "rare", "one of a kind",

        # Potentially problematic
        "sexy", "adult", "explicit", "nsfw",
    ]

    # Extended niche data with search-focused keywords
    NICHE_DATA = {
        # Beverages
        "coffee": {
            "keywords": ["coffee lover", "caffeine addict", "espresso", "latte", "barista life", "coffee obsessed", "morning coffee", "coffee humor"],
            "search_terms": ["coffee gifts", "caffeine lover", "espresso fan", "coffee addict gift", "barista appreciation"],
            "audience": ["coffee enthusiasts", "caffeine lovers", "baristas", "morning people"],
        },
        "tea": {
            "keywords": ["tea lover", "tea time", "herbal tea", "chai", "tea addict", "tea obsessed"],
            "search_terms": ["tea gifts", "tea lover present", "chai enthusiast", "herbal tea fan"],
            "audience": ["tea lovers", "chai enthusiasts", "herbal tea fans"],
        },
        "beer": {
            "keywords": ["craft beer", "beer lover", "hops", "IPA fan", "brewery", "beer snob", "beer enthusiast"],
            "search_terms": ["beer gifts", "craft beer lover", "IPA enthusiast", "brewery fan"],
            "audience": ["beer lovers", "craft beer enthusiasts", "IPA fans", "brewery visitors"],
        },
        "wine": {
            "keywords": ["wine lover", "vino", "wine mom", "wine dad", "sommelier", "wine enthusiast", "wine time"],
            "search_terms": ["wine gifts", "wine lover present", "vino enthusiast", "wine mom gift"],
            "audience": ["wine lovers", "wine enthusiasts", "sommeliers"],
        },
        "whiskey": {
            "keywords": ["whiskey lover", "bourbon fan", "scotch", "whiskey enthusiast", "on the rocks"],
            "search_terms": ["whiskey gifts", "bourbon lover", "scotch enthusiast"],
            "audience": ["whiskey lovers", "bourbon fans", "scotch enthusiasts"],
        },

        # Fitness & Sports
        "fitness": {
            "keywords": ["gym life", "workout", "gains", "lifting", "fitness motivation", "gym rat", "beast mode"],
            "search_terms": ["fitness gifts", "gym lover", "workout motivation", "lifting enthusiast"],
            "audience": ["gym enthusiasts", "fitness lovers", "bodybuilders", "personal trainers"],
        },
        "yoga": {
            "keywords": ["yoga lover", "namaste", "yoga life", "zen", "meditation", "yoga instructor", "yogi"],
            "search_terms": ["yoga gifts", "yogi present", "meditation lover", "zen enthusiast"],
            "audience": ["yoga practitioners", "meditation lovers", "yoga instructors"],
        },
        "running": {
            "keywords": ["runner", "marathon", "jogging", "run life", "trail running", "5K", "runner's high"],
            "search_terms": ["runner gifts", "marathon present", "jogging enthusiast", "trail runner"],
            "audience": ["runners", "marathon runners", "joggers", "trail runners"],
        },
        "crossfit": {
            "keywords": ["crossfit", "WOD", "box life", "crossfit athlete", "functional fitness"],
            "search_terms": ["crossfit gifts", "WOD lover", "crossfit enthusiast"],
            "audience": ["crossfit athletes", "functional fitness fans"],
        },
        "cycling": {
            "keywords": ["cyclist", "bike life", "cycling", "road bike", "mountain bike", "spin class"],
            "search_terms": ["cyclist gifts", "biking enthusiast", "cycling lover"],
            "audience": ["cyclists", "bikers", "spin enthusiasts"],
        },
        "swimming": {
            "keywords": ["swimmer", "pool life", "swim team", "water lover", "lap swimmer"],
            "search_terms": ["swimmer gifts", "swimming enthusiast", "pool lover"],
            "audience": ["swimmers", "water sports enthusiasts"],
        },
        "golf": {
            "keywords": ["golfer", "golf life", "on the green", "golf addict", "tee time", "golf humor"],
            "search_terms": ["golfer gifts", "golf enthusiast", "golf lover present"],
            "audience": ["golfers", "golf enthusiasts", "weekend golfers"],
        },
        "tennis": {
            "keywords": ["tennis player", "tennis life", "love-love", "tennis enthusiast"],
            "search_terms": ["tennis gifts", "tennis lover", "tennis player present"],
            "audience": ["tennis players", "tennis enthusiasts"],
        },
        "basketball": {
            "keywords": ["basketball", "hoops", "baller", "court life", "basketball player"],
            "search_terms": ["basketball gifts", "hoops lover", "baller present"],
            "audience": ["basketball players", "hoops enthusiasts"],
        },
        "football": {
            "keywords": ["football", "gridiron", "touchdown", "football fan", "game day"],
            "search_terms": ["football gifts", "gridiron fan", "football enthusiast"],
            "audience": ["football fans", "game day enthusiasts"],
        },
        "soccer": {
            "keywords": ["soccer", "futbol", "soccer player", "pitch life", "soccer mom", "soccer dad"],
            "search_terms": ["soccer gifts", "futbol lover", "soccer parent"],
            "audience": ["soccer players", "soccer parents", "futbol fans"],
        },
        "baseball": {
            "keywords": ["baseball", "softball", "diamond life", "baseball player", "home run"],
            "search_terms": ["baseball gifts", "softball lover", "baseball fan"],
            "audience": ["baseball players", "softball players", "baseball fans"],
        },
        "hockey": {
            "keywords": ["hockey", "ice hockey", "hockey player", "puck life", "hockey mom", "hockey dad"],
            "search_terms": ["hockey gifts", "hockey enthusiast", "hockey parent"],
            "audience": ["hockey players", "hockey parents", "ice hockey fans"],
        },
        "volleyball": {
            "keywords": ["volleyball", "volleyball player", "beach volleyball", "spike life"],
            "search_terms": ["volleyball gifts", "volleyball lover", "beach volleyball fan"],
            "audience": ["volleyball players", "beach volleyball enthusiasts"],
        },
        "wrestling": {
            "keywords": ["wrestling", "wrestler", "mat life", "wrestling coach", "wrestling mom"],
            "search_terms": ["wrestling gifts", "wrestler present", "wrestling parent"],
            "audience": ["wrestlers", "wrestling coaches", "wrestling parents"],
        },
        "mma": {
            "keywords": ["MMA", "mixed martial arts", "UFC fan", "fighter", "jiu jitsu", "muay thai"],
            "search_terms": ["MMA gifts", "UFC fan present", "martial arts lover"],
            "audience": ["MMA fans", "martial artists", "UFC enthusiasts"],
        },
        "boxing": {
            "keywords": ["boxing", "boxer", "fight life", "boxing gym", "knockout"],
            "search_terms": ["boxing gifts", "boxer present", "fight fan"],
            "audience": ["boxers", "boxing fans", "fight enthusiasts"],
        },

        # Outdoor Activities
        "fishing": {
            "keywords": ["fishing", "angler", "bass fishing", "fly fishing", "fisherman", "reel life", "gone fishing"],
            "search_terms": ["fishing gifts", "angler present", "fisherman gift", "bass fishing lover"],
            "audience": ["anglers", "fishermen", "bass fishers", "fly fishing enthusiasts"],
        },
        "hunting": {
            "keywords": ["hunting", "hunter", "deer hunting", "duck hunting", "bow hunter", "hunt life"],
            "search_terms": ["hunting gifts", "hunter present", "deer hunter gift", "bow hunting lover"],
            "audience": ["hunters", "deer hunters", "duck hunters", "bow hunters"],
        },
        "camping": {
            "keywords": ["camping", "camper", "camp life", "tent life", "happy camper", "campfire", "glamping"],
            "search_terms": ["camping gifts", "camper present", "outdoor lover gift"],
            "audience": ["campers", "outdoor enthusiasts", "glamping lovers"],
        },
        "hiking": {
            "keywords": ["hiking", "hiker", "trail life", "mountain lover", "nature", "take a hike", "trail blazer"],
            "search_terms": ["hiking gifts", "hiker present", "trail lover gift", "mountain enthusiast"],
            "audience": ["hikers", "trail enthusiasts", "mountain lovers"],
        },
        "climbing": {
            "keywords": ["rock climbing", "climber", "bouldering", "mountain climbing", "climb life"],
            "search_terms": ["climbing gifts", "rock climber present", "bouldering enthusiast"],
            "audience": ["rock climbers", "boulderers", "mountain climbers"],
        },
        "kayaking": {
            "keywords": ["kayaking", "kayaker", "paddle life", "kayak lover", "water sports"],
            "search_terms": ["kayaking gifts", "kayaker present", "paddle enthusiast"],
            "audience": ["kayakers", "paddle sports enthusiasts"],
        },
        "surfing": {
            "keywords": ["surfing", "surfer", "surf life", "wave rider", "beach life", "surf vibes"],
            "search_terms": ["surfing gifts", "surfer present", "wave lover gift"],
            "audience": ["surfers", "wave riders", "beach enthusiasts"],
        },
        "skiing": {
            "keywords": ["skiing", "skier", "ski life", "powder", "slopes", "ski bum", "après ski"],
            "search_terms": ["skiing gifts", "skier present", "powder lover gift"],
            "audience": ["skiers", "powder enthusiasts", "ski bums"],
        },
        "snowboarding": {
            "keywords": ["snowboarding", "snowboarder", "shred life", "powder", "board life"],
            "search_terms": ["snowboarding gifts", "snowboarder present", "shred enthusiast"],
            "audience": ["snowboarders", "shred enthusiasts"],
        },
        "sailing": {
            "keywords": ["sailing", "sailor", "boat life", "yacht", "nautical", "anchors away"],
            "search_terms": ["sailing gifts", "sailor present", "nautical lover gift"],
            "audience": ["sailors", "boat enthusiasts", "nautical lovers"],
        },
        "boating": {
            "keywords": ["boating", "boat life", "captain", "lake life", "river life", "pontoon"],
            "search_terms": ["boating gifts", "boat lover present", "captain gift"],
            "audience": ["boaters", "lake lovers", "boat captains"],
        },
        "rv": {
            "keywords": ["RV life", "RV living", "camper life", "road trip", "full-time RV", "nomad life"],
            "search_terms": ["RV gifts", "RV enthusiast present", "road trip lover"],
            "audience": ["RV enthusiasts", "full-time RVers", "road trippers"],
        },
        "atv": {
            "keywords": ["ATV", "four wheeler", "off-road", "mud life", "trail riding", "side by side"],
            "search_terms": ["ATV gifts", "off-road enthusiast", "mud lover"],
            "audience": ["ATV riders", "off-road enthusiasts", "mud lovers"],
        },
        "motorcycle": {
            "keywords": ["motorcycle", "biker", "ride life", "two wheels", "motorcycle life", "open road"],
            "search_terms": ["motorcycle gifts", "biker present", "rider gift"],
            "audience": ["bikers", "motorcycle enthusiasts", "riders"],
        },

        # Pets
        "dogs": {
            "keywords": ["dog lover", "dog mom", "dog dad", "fur baby", "puppy love", "dog life", "rescue dog"],
            "search_terms": ["dog lover gifts", "dog mom present", "dog dad gift", "puppy enthusiast"],
            "audience": ["dog lovers", "dog moms", "dog dads", "pet parents"],
        },
        "cats": {
            "keywords": ["cat lover", "cat mom", "cat dad", "crazy cat lady", "kitten", "cat life", "meow"],
            "search_terms": ["cat lover gifts", "cat mom present", "cat dad gift", "kitten enthusiast"],
            "audience": ["cat lovers", "cat moms", "cat dads", "feline enthusiasts"],
        },
        "horses": {
            "keywords": ["horse lover", "equestrian", "horse mom", "barn life", "horse girl", "riding"],
            "search_terms": ["horse gifts", "equestrian present", "horse mom gift"],
            "audience": ["horse lovers", "equestrians", "barn enthusiasts"],
        },
        "chickens": {
            "keywords": ["chicken lover", "chicken mom", "backyard chickens", "crazy chicken lady", "farm life"],
            "search_terms": ["chicken gifts", "chicken mom present", "backyard farmer"],
            "audience": ["chicken keepers", "backyard farmers", "poultry enthusiasts"],
        },
        "goats": {
            "keywords": ["goat lover", "goat mom", "crazy goat lady", "farm life", "goat life"],
            "search_terms": ["goat gifts", "goat mom present", "farm animal lover"],
            "audience": ["goat keepers", "goat lovers", "farm enthusiasts"],
        },
        "reptiles": {
            "keywords": ["reptile lover", "snake owner", "lizard lover", "reptile mom", "cold blooded"],
            "search_terms": ["reptile gifts", "snake lover present", "lizard enthusiast"],
            "audience": ["reptile owners", "snake enthusiasts", "lizard lovers"],
        },
        "birds": {
            "keywords": ["bird lover", "parrot owner", "bird mom", "bird dad", "bird watching", "birder"],
            "search_terms": ["bird gifts", "parrot lover present", "bird watcher gift"],
            "audience": ["bird lovers", "parrot owners", "bird watchers"],
        },
        "fish": {
            "keywords": ["aquarium lover", "fish keeper", "reef tank", "tropical fish", "aquarist"],
            "search_terms": ["aquarium gifts", "fish keeper present", "reef tank enthusiast"],
            "audience": ["aquarists", "fish keepers", "reef enthusiasts"],
        },

        # Professions
        "nursing": {
            "keywords": ["nurse life", "RN", "nursing", "night shift", "scrub life", "nurse hero", "healthcare"],
            "search_terms": ["nurse gifts", "RN present", "nursing school", "healthcare worker gift"],
            "audience": ["nurses", "RNs", "nursing students", "healthcare workers"],
        },
        "doctor": {
            "keywords": ["doctor", "MD", "physician", "medical", "doctor life", "future doctor"],
            "search_terms": ["doctor gifts", "physician present", "medical school gift"],
            "audience": ["doctors", "physicians", "medical students"],
        },
        "emt": {
            "keywords": ["EMT", "paramedic", "first responder", "ambulance", "EMS life"],
            "search_terms": ["EMT gifts", "paramedic present", "first responder gift"],
            "audience": ["EMTs", "paramedics", "first responders"],
        },
        "firefighter": {
            "keywords": ["firefighter", "fire department", "fireman", "fire life", "thin red line"],
            "search_terms": ["firefighter gifts", "fireman present", "fire department gift"],
            "audience": ["firefighters", "fire department members"],
        },
        "police": {
            "keywords": ["police", "cop", "law enforcement", "thin blue line", "police life", "LEO"],
            "search_terms": ["police gifts", "law enforcement present", "cop gift"],
            "audience": ["police officers", "law enforcement", "LEOs"],
        },
        "military": {
            "keywords": ["military", "veteran", "army", "navy", "marines", "air force", "served"],
            "search_terms": ["military gifts", "veteran present", "armed forces gift"],
            "audience": ["military members", "veterans", "service members"],
        },
        "teaching": {
            "keywords": ["teacher life", "educator", "teaching", "classroom", "teacher appreciation", "best teacher"],
            "search_terms": ["teacher gifts", "educator present", "classroom gift", "teaching appreciation"],
            "audience": ["teachers", "educators", "professors", "teaching assistants"],
        },
        "principal": {
            "keywords": ["principal", "school administrator", "school leader", "principal life"],
            "search_terms": ["principal gifts", "school administrator present"],
            "audience": ["principals", "school administrators"],
        },
        "librarian": {
            "keywords": ["librarian", "book lover", "library life", "reading", "librarian life"],
            "search_terms": ["librarian gifts", "library lover present"],
            "audience": ["librarians", "library workers"],
        },
        "mechanic": {
            "keywords": ["mechanic", "auto mechanic", "car guy", "grease monkey", "garage life", "wrench life"],
            "search_terms": ["mechanic gifts", "auto mechanic present", "car enthusiast gift"],
            "audience": ["mechanics", "auto workers", "car enthusiasts"],
        },
        "electrician": {
            "keywords": ["electrician", "sparky", "electrical", "electrician life", "watts up"],
            "search_terms": ["electrician gifts", "sparky present", "electrical worker gift"],
            "audience": ["electricians", "electrical workers"],
        },
        "plumber": {
            "keywords": ["plumber", "plumbing", "pipe fitter", "plumber life"],
            "search_terms": ["plumber gifts", "plumbing present"],
            "audience": ["plumbers", "pipe fitters"],
        },
        "carpenter": {
            "keywords": ["carpenter", "woodworker", "wood life", "saw dust", "carpenter life"],
            "search_terms": ["carpenter gifts", "woodworker present"],
            "audience": ["carpenters", "woodworkers"],
        },
        "welder": {
            "keywords": ["welder", "welding", "welder life", "sparks fly", "fabricator"],
            "search_terms": ["welder gifts", "welding present", "fabricator gift"],
            "audience": ["welders", "fabricators"],
        },
        "trucker": {
            "keywords": ["trucker", "truck driver", "big rig", "18 wheeler", "trucker life", "road warrior"],
            "search_terms": ["trucker gifts", "truck driver present", "big rig gift"],
            "audience": ["truckers", "truck drivers", "CDL holders"],
        },
        "pilot": {
            "keywords": ["pilot", "aviator", "flying", "pilot life", "aviation", "airplane"],
            "search_terms": ["pilot gifts", "aviator present", "aviation enthusiast"],
            "audience": ["pilots", "aviators", "aviation enthusiasts"],
        },
        "chef": {
            "keywords": ["chef", "cook", "culinary", "chef life", "kitchen life", "foodie"],
            "search_terms": ["chef gifts", "cook present", "culinary enthusiast"],
            "audience": ["chefs", "cooks", "culinary professionals"],
        },
        "bartender": {
            "keywords": ["bartender", "mixologist", "bar life", "cocktails", "bartender life"],
            "search_terms": ["bartender gifts", "mixologist present"],
            "audience": ["bartenders", "mixologists"],
        },
        "hairstylist": {
            "keywords": ["hairstylist", "hair dresser", "salon life", "beautician", "stylist life"],
            "search_terms": ["hairstylist gifts", "salon worker present"],
            "audience": ["hairstylists", "beauticians", "salon workers"],
        },
        "realtor": {
            "keywords": ["realtor", "real estate", "real estate agent", "realtor life", "home sales"],
            "search_terms": ["realtor gifts", "real estate agent present"],
            "audience": ["realtors", "real estate agents"],
        },
        "accountant": {
            "keywords": ["accountant", "CPA", "accounting", "tax season", "number cruncher"],
            "search_terms": ["accountant gifts", "CPA present", "tax season gift"],
            "audience": ["accountants", "CPAs", "bookkeepers"],
        },
        "lawyer": {
            "keywords": ["lawyer", "attorney", "legal", "law school", "lawyer life", "esquire"],
            "search_terms": ["lawyer gifts", "attorney present", "law school gift"],
            "audience": ["lawyers", "attorneys", "law students"],
        },
        "engineer": {
            "keywords": ["engineer", "engineering", "engineer life", "problem solver", "STEM"],
            "search_terms": ["engineer gifts", "engineering present", "STEM gift"],
            "audience": ["engineers", "engineering students"],
        },
        "programmer": {
            "keywords": ["programmer", "developer", "coder", "coding", "software", "debug life", "git commit"],
            "search_terms": ["programmer gifts", "developer present", "coder gift"],
            "audience": ["programmers", "developers", "software engineers"],
        },
        "scientist": {
            "keywords": ["scientist", "science", "research", "lab life", "STEM", "scientist life"],
            "search_terms": ["scientist gifts", "science lover present", "research gift"],
            "audience": ["scientists", "researchers", "lab workers"],
        },
        "pharmacist": {
            "keywords": ["pharmacist", "pharmacy", "pharmacist life", "pill counter", "healthcare"],
            "search_terms": ["pharmacist gifts", "pharmacy present"],
            "audience": ["pharmacists", "pharmacy techs"],
        },
        "dentist": {
            "keywords": ["dentist", "dental", "dentist life", "tooth fairy", "dental hygienist"],
            "search_terms": ["dentist gifts", "dental worker present"],
            "audience": ["dentists", "dental hygienists"],
        },
        "veterinarian": {
            "keywords": ["veterinarian", "vet", "vet life", "animal doctor", "vet tech"],
            "search_terms": ["veterinarian gifts", "vet present", "vet tech gift"],
            "audience": ["veterinarians", "vet techs", "animal care workers"],
        },
        "dispatcher": {
            "keywords": ["dispatcher", "911 dispatcher", "dispatch life", "thin gold line", "first responder"],
            "search_terms": ["dispatcher gifts", "911 operator present"],
            "audience": ["dispatchers", "911 operators"],
        },
        "correctional": {
            "keywords": ["correctional officer", "CO", "prison guard", "corrections", "thin silver line"],
            "search_terms": ["correctional officer gifts", "CO present"],
            "audience": ["correctional officers", "prison staff"],
        },
        "farmer": {
            "keywords": ["farmer", "farm life", "farming", "agriculture", "rancher", "tractor life"],
            "search_terms": ["farmer gifts", "farm life present", "agriculture gift"],
            "audience": ["farmers", "ranchers", "agricultural workers"],
        },

        # Family & Parenting
        "parenting": {
            "keywords": ["parent life", "mom life", "dad life", "parenting", "tired parent", "raising kids"],
            "search_terms": ["parenting gifts", "parent present", "mom dad gift"],
            "audience": ["parents", "moms", "dads"],
        },
        "mom": {
            "keywords": ["mom life", "mama", "mother", "mommy", "mom mode", "super mom", "tired mom"],
            "search_terms": ["mom gifts", "mother present", "mama gift"],
            "audience": ["moms", "mothers", "new moms"],
        },
        "dad": {
            "keywords": ["dad life", "papa", "father", "daddy", "dad jokes", "super dad", "best dad"],
            "search_terms": ["dad gifts", "father present", "papa gift"],
            "audience": ["dads", "fathers", "new dads"],
        },
        "grandparent": {
            "keywords": ["grandma", "grandpa", "nana", "papa", "grandparent life", "best grandma", "best grandpa"],
            "search_terms": ["grandparent gifts", "grandma present", "grandpa gift"],
            "audience": ["grandparents", "grandmas", "grandpas"],
        },
        "aunt": {
            "keywords": ["aunt", "auntie", "aunt life", "best aunt", "cool aunt", "aunt vibes"],
            "search_terms": ["aunt gifts", "auntie present", "aunt appreciation"],
            "audience": ["aunts", "aunties"],
        },
        "uncle": {
            "keywords": ["uncle", "funcle", "uncle life", "best uncle", "cool uncle"],
            "search_terms": ["uncle gifts", "funcle present"],
            "audience": ["uncles"],
        },
        "twins": {
            "keywords": ["twin", "twins", "twin life", "twin mom", "twin dad", "double trouble"],
            "search_terms": ["twin gifts", "twin parent present"],
            "audience": ["twin parents", "twins"],
        },

        # Hobbies
        "gaming": {
            "keywords": ["gamer", "gaming life", "video games", "player one", "level up", "respawn", "game on"],
            "search_terms": ["gamer gifts", "gaming present", "video game lover gift"],
            "audience": ["gamers", "video game enthusiasts", "streamers"],
        },
        "reading": {
            "keywords": ["book lover", "bookworm", "reading", "bibliophile", "book nerd", "one more chapter"],
            "search_terms": ["book lover gifts", "reading present", "bibliophile gift"],
            "audience": ["book lovers", "readers", "bibliophiles"],
        },
        "writing": {
            "keywords": ["writer", "author", "writing life", "novelist", "storyteller", "writer life"],
            "search_terms": ["writer gifts", "author present", "writing enthusiast"],
            "audience": ["writers", "authors", "aspiring writers"],
        },
        "photography": {
            "keywords": ["photographer", "photography", "camera life", "shutterbug", "photo life"],
            "search_terms": ["photographer gifts", "camera lover present"],
            "audience": ["photographers", "camera enthusiasts"],
        },
        "gardening": {
            "keywords": ["gardener", "gardening", "plant life", "green thumb", "garden life", "plant lover"],
            "search_terms": ["gardener gifts", "plant lover present", "garden enthusiast"],
            "audience": ["gardeners", "plant lovers", "green thumbs"],
        },
        "plants": {
            "keywords": ["plant mom", "plant dad", "plant parent", "crazy plant lady", "plant obsessed"],
            "search_terms": ["plant lover gifts", "plant parent present"],
            "audience": ["plant parents", "plant lovers"],
        },
        "cooking": {
            "keywords": ["home cook", "cooking", "kitchen life", "foodie", "home chef", "grill master"],
            "search_terms": ["home cook gifts", "cooking enthusiast present"],
            "audience": ["home cooks", "foodies", "grill masters"],
        },
        "baking": {
            "keywords": ["baker", "baking", "pastry", "cupcakes", "baker life", "baking queen"],
            "search_terms": ["baker gifts", "baking enthusiast present"],
            "audience": ["bakers", "pastry enthusiasts"],
        },
        "crafting": {
            "keywords": ["crafter", "crafting", "DIY", "handmade", "craft life", "maker"],
            "search_terms": ["crafter gifts", "DIY enthusiast present"],
            "audience": ["crafters", "DIY enthusiasts", "makers"],
        },
        "knitting": {
            "keywords": ["knitter", "knitting", "yarn life", "knitting addict", "yarn lover"],
            "search_terms": ["knitter gifts", "yarn lover present"],
            "audience": ["knitters", "yarn enthusiasts"],
        },
        "sewing": {
            "keywords": ["sewer", "sewing", "quilter", "quilting", "fabric lover", "sewing life"],
            "search_terms": ["sewing gifts", "quilter present"],
            "audience": ["sewers", "quilters"],
        },
        "woodworking": {
            "keywords": ["woodworker", "woodworking", "sawdust", "wood life", "workshop"],
            "search_terms": ["woodworker gifts", "woodworking enthusiast"],
            "audience": ["woodworkers", "workshop enthusiasts"],
        },
        "painting": {
            "keywords": ["artist", "painter", "painting", "art life", "creative", "paint life"],
            "search_terms": ["artist gifts", "painter present"],
            "audience": ["artists", "painters"],
        },
        "music": {
            "keywords": ["musician", "music lover", "music life", "band", "jam session", "music is life"],
            "search_terms": ["musician gifts", "music lover present"],
            "audience": ["musicians", "music lovers"],
        },
        "guitar": {
            "keywords": ["guitarist", "guitar player", "guitar life", "rock on", "acoustic", "electric"],
            "search_terms": ["guitarist gifts", "guitar player present"],
            "audience": ["guitarists", "guitar players"],
        },
        "drums": {
            "keywords": ["drummer", "drums", "drum life", "beat maker", "percussion"],
            "search_terms": ["drummer gifts", "drum player present"],
            "audience": ["drummers", "percussionists"],
        },
        "piano": {
            "keywords": ["pianist", "piano", "piano player", "keys", "piano life"],
            "search_terms": ["pianist gifts", "piano player present"],
            "audience": ["pianists", "piano players"],
        },
        "vinyl": {
            "keywords": ["vinyl collector", "record collector", "vinyl life", "audiophile", "turntable"],
            "search_terms": ["vinyl collector gifts", "record lover present"],
            "audience": ["vinyl collectors", "audiophiles"],
        },
        "podcasting": {
            "keywords": ["podcaster", "podcast", "podcast life", "content creator", "on air"],
            "search_terms": ["podcaster gifts", "content creator present"],
            "audience": ["podcasters", "content creators"],
        },
        "streaming": {
            "keywords": ["streamer", "streaming", "twitch", "live streaming", "content creator"],
            "search_terms": ["streamer gifts", "content creator present"],
            "audience": ["streamers", "content creators"],
        },
        "astronomy": {
            "keywords": ["astronomer", "stargazer", "space lover", "astronomy", "cosmos", "night sky"],
            "search_terms": ["astronomer gifts", "stargazer present", "space enthusiast"],
            "audience": ["astronomers", "stargazers", "space enthusiasts"],
        },
        "travel": {
            "keywords": ["traveler", "wanderlust", "adventure", "explorer", "travel life", "jet setter"],
            "search_terms": ["traveler gifts", "wanderlust present", "adventure lover"],
            "audience": ["travelers", "adventurers", "explorers"],
        },
        "cars": {
            "keywords": ["car lover", "car enthusiast", "gearhead", "car life", "auto", "muscle car"],
            "search_terms": ["car lover gifts", "gearhead present", "auto enthusiast"],
            "audience": ["car enthusiasts", "gearheads", "auto lovers"],
        },
        "trucks": {
            "keywords": ["truck lover", "truck life", "pickup", "diesel", "truck guy"],
            "search_terms": ["truck lover gifts", "pickup enthusiast"],
            "audience": ["truck lovers", "diesel enthusiasts"],
        },
        "jeep": {
            "keywords": ["jeep lover", "jeep life", "jeep girl", "jeep guy", "off road", "mudding"],
            "search_terms": ["jeep lover gifts", "jeep enthusiast"],
            "audience": ["jeep lovers", "off-road enthusiasts"],
        },
        "rc": {
            "keywords": ["RC", "remote control", "RC car", "RC plane", "RC enthusiast"],
            "search_terms": ["RC gifts", "remote control enthusiast"],
            "audience": ["RC hobbyists", "remote control enthusiasts"],
        },
        "drone": {
            "keywords": ["drone pilot", "drone", "aerial", "FPV", "drone life"],
            "search_terms": ["drone gifts", "drone pilot present"],
            "audience": ["drone pilots", "aerial photographers"],
        },
        "anime": {
            "keywords": ["anime", "otaku", "manga", "anime lover", "weeb", "anime life"],
            "search_terms": ["anime gifts", "otaku present", "manga lover"],
            "audience": ["anime fans", "otakus", "manga lovers"],
        },
        "comics": {
            "keywords": ["comic fan", "comic collector", "geek", "nerd", "superhero"],
            "search_terms": ["comic gifts", "geek present", "nerd gift"],
            "audience": ["comic fans", "collectors", "geeks"],
        },
        "boardgames": {
            "keywords": ["board gamer", "tabletop", "board game", "game night", "dice", "D&D"],
            "search_terms": ["board gamer gifts", "tabletop present"],
            "audience": ["board gamers", "tabletop enthusiasts"],
        },
        "poker": {
            "keywords": ["poker player", "poker", "card shark", "all in", "casino"],
            "search_terms": ["poker gifts", "card player present"],
            "audience": ["poker players", "card enthusiasts"],
        },

        # Lifestyle
        "introvert": {
            "keywords": ["introvert", "homebody", "anti social", "leave me alone", "introvert life"],
            "search_terms": ["introvert gifts", "homebody present"],
            "audience": ["introverts", "homebodies"],
        },
        "extrovert": {
            "keywords": ["extrovert", "social butterfly", "people person", "extrovert life"],
            "search_terms": ["extrovert gifts", "social butterfly present"],
            "audience": ["extroverts", "social butterflies"],
        },
        "anxiety": {
            "keywords": ["anxiety", "anxious", "mental health", "overthinking", "anxiety warrior"],
            "search_terms": ["anxiety awareness gifts", "mental health present"],
            "audience": ["anxiety warriors", "mental health advocates"],
        },
        "sarcasm": {
            "keywords": ["sarcasm", "sarcastic", "fluent in sarcasm", "sarcasm is my love language"],
            "search_terms": ["sarcastic gifts", "sarcasm lover present"],
            "audience": ["sarcastic people", "humor lovers"],
        },
        "true crime": {
            "keywords": ["true crime", "crime junkie", "murder mystery", "true crime addict"],
            "search_terms": ["true crime gifts", "crime junkie present"],
            "audience": ["true crime fans", "crime junkies"],
        },
        "astrology": {
            "keywords": ["astrology", "zodiac", "horoscope", "star sign", "mercury retrograde"],
            "search_terms": ["astrology gifts", "zodiac present"],
            "audience": ["astrology enthusiasts", "zodiac lovers"],
        },
        "meditation": {
            "keywords": ["meditation", "mindfulness", "zen", "peaceful", "inner peace", "namaste"],
            "search_terms": ["meditation gifts", "mindfulness present"],
            "audience": ["meditation practitioners", "mindfulness enthusiasts"],
        },
        "vegan": {
            "keywords": ["vegan", "plant based", "vegan life", "animal lover", "cruelty free"],
            "search_terms": ["vegan gifts", "plant based present"],
            "audience": ["vegans", "plant-based enthusiasts"],
        },
        "keto": {
            "keywords": ["keto", "ketogenic", "low carb", "keto life", "keto diet"],
            "search_terms": ["keto gifts", "low carb present"],
            "audience": ["keto dieters", "low carb enthusiasts"],
        },
        "vintage": {
            "keywords": ["vintage", "retro", "old school", "classic", "throwback", "nostalgic"],
            "search_terms": ["vintage gifts", "retro present"],
            "audience": ["vintage lovers", "retro enthusiasts"],
        },
        "minimalist": {
            "keywords": ["minimalist", "simple life", "less is more", "minimal"],
            "search_terms": ["minimalist gifts", "simple life present"],
            "audience": ["minimalists", "simple living enthusiasts"],
        },
    }

    # Generic data for unknown niches
    GENERIC_DATA = {
        "keywords": ["funny", "humor", "quote", "saying", "gift idea", "cool", "awesome"],
        "search_terms": ["funny gifts", "humor present", "quote lover"],
        "audience": ["gift seekers", "humor lovers"],
    }

    def generate(
        self,
        phrase: str,
        niche: Optional[str] = None,
        tone: str = "neutral"
    ) -> Dict[str, Any]:
        """Generate TOS-compliant, design-focused listing."""
        result = {
            "title": "",
            "bullet_1": "",
            "bullet_2": "",
            "description": "",
            "backend_keywords": "",
            "is_compliant": True,
            "warnings": []
        }

        clean_phrase = self._clean_phrase(phrase)
        niche_data = self._get_niche_data(niche)

        # Generate each field - NO PRODUCT MENTIONS
        result["title"] = self._generate_title(clean_phrase, niche, niche_data)
        result["bullet_1"] = self._generate_bullet_1(clean_phrase, niche_data)
        result["bullet_2"] = self._generate_bullet_2(clean_phrase, niche_data)
        result["description"] = self._generate_description(clean_phrase, niche, niche_data)
        result["backend_keywords"] = self._generate_backend_keywords(clean_phrase, niche_data)

        # Validate
        validation = self.validate_listing(
            result["title"],
            result["bullet_1"],
            result["bullet_2"],
            result["description"],
            result["backend_keywords"]
        )
        result["is_compliant"] = validation["is_compliant"]
        result["warnings"] = validation["issues"]

        return result

    def _clean_phrase(self, phrase: str) -> str:
        """Clean phrase for use in listings."""
        forbidden = set(self.FORBIDDEN_WORDS)
        words = phrase.split()
        clean_words = [w for w in words if w.lower() not in forbidden]
        return ' '.join(clean_words) if clean_words else phrase

    def _get_niche_data(self, niche: Optional[str]) -> Dict:
        """Get niche-specific data."""
        if niche and niche.lower() in self.NICHE_DATA:
            return self.NICHE_DATA[niche.lower()]
        return self.GENERIC_DATA

    def _generate_title(self, phrase: str, niche: Optional[str], niche_data: Dict) -> str:
        """Generate search-optimized title (max 80 chars) - NO PRODUCT WORDS."""
        phrase_title = phrase.title()
        niche_display = niche.title() if niche else ""

        # Try patterns that fit
        if niche_display:
            patterns = [
                f"{phrase_title} Funny {niche_display} Quote Gift Idea",
                f"{phrase_title} - {niche_display} Lover Gift",
                f"Funny {niche_display} {phrase_title} Quote",
                f"{phrase_title} {niche_display} Humor",
                f"{phrase_title} - Gift For {niche_display} Lovers",
                f"{phrase_title}",
            ]
        else:
            patterns = [
                f"{phrase_title} Funny Quote Gift Idea",
                f"{phrase_title} Humor Quote",
                f"Funny {phrase_title} Quote",
                f"{phrase_title}",
            ]

        for pattern in patterns:
            if len(pattern) <= 80:
                return pattern

        return phrase_title[:77] + "..."

    def _generate_bullet_1(self, phrase: str, niche_data: Dict) -> str:
        """Generate first bullet - search intent focused, NO PRODUCT INFO."""
        audience = niche_data["audience"][:3]
        audience_str = ", ".join(audience)
        search_terms = niche_data.get("search_terms", niche_data["keywords"])[:2]

        bullet = f"Looking for {search_terms[0]}? This \"{phrase}\" design is perfect for {audience_str}. Makes an ideal gift for birthdays, Christmas, Mother's Day, Father's Day, or any special occasion."

        return bullet[:256] if len(bullet) > 256 else bullet

    def _generate_bullet_2(self, phrase: str, niche_data: Dict) -> str:
        """Generate second bullet - design and audience focused, NO PRODUCT INFO."""
        keywords = niche_data["keywords"][:3]

        bullet = f"Show your personality with this unique design. Perfect for anyone who loves {', '.join(keywords)}. A great way to express yourself and start conversations."

        return bullet[:256] if len(bullet) > 256 else bullet

    def _generate_description(self, phrase: str, niche: Optional[str], niche_data: Dict) -> str:
        """Generate search-focused description - NO PRODUCT INFO."""
        audience = niche_data["audience"][:3]
        keywords = niche_data["keywords"][:4]
        search_terms = niche_data.get("search_terms", keywords)[:3]

        niche_name = niche.lower() if niche else "unique designs"

        description = f"""Looking for the perfect gift? The "{phrase}" design captures exactly what {niche_name} enthusiasts love to express!

This eye-catching design makes a wonderful gift for {', '.join(audience)}. Whether you're searching for {', '.join(search_terms)}, this is the perfect choice.

Ideal for:
- Birthday gifts
- Christmas presents
- Mother's Day or Father's Day
- Thank you gifts
- Just because surprises

Keywords: {', '.join(keywords[:6])}

This design is sure to get compliments and start conversations. Show the world your passion for {niche_name} with this unique and memorable design!"""

        return description[:2000] if len(description) > 2000 else description

    def _generate_backend_keywords(self, phrase: str, niche_data: Dict) -> str:
        """Generate backend search keywords (max 250 chars)."""
        phrase_words = [w.lower() for w in phrase.split() if len(w) > 2]
        niche_keywords = niche_data["keywords"][:6]
        search_terms = niche_data.get("search_terms", [])[:4]

        gift_keywords = ["gift", "present", "birthday", "christmas", "funny", "humor", "quote"]

        all_keywords = []
        seen = set()
        forbidden = set(w.lower() for w in self.FORBIDDEN_WORDS)

        for kw in phrase_words + niche_keywords + search_terms + gift_keywords:
            kw_lower = kw.lower()
            if kw_lower not in seen and kw_lower not in forbidden:
                seen.add(kw_lower)
                all_keywords.append(kw_lower)

        result = ' '.join(all_keywords)
        if len(result) > 250:
            result = result[:250].rsplit(' ', 1)[0]

        return result

    def validate_listing(
        self,
        title: str,
        bullet_1: str = None,
        bullet_2: str = None,
        description: str = None,
        backend_keywords: str = None
    ) -> Dict[str, Any]:
        """Validate listing against Amazon Merch TOS."""
        issues = []

        all_content = ' '.join(filter(None, [title, bullet_1, bullet_2, description])).lower()

        for word in self.FORBIDDEN_WORDS:
            if re.search(rf'\b{re.escape(word)}\b', all_content):
                issues.append(f"Contains forbidden word: '{word}'")

        if title and len(title) > 80:
            issues.append(f"Title too long: {len(title)}/80 characters")

        if bullet_1 and len(bullet_1) > 256:
            issues.append(f"Bullet 1 too long: {len(bullet_1)}/256 characters")

        if bullet_2 and len(bullet_2) > 256:
            issues.append(f"Bullet 2 too long: {len(bullet_2)}/256 characters")

        if description and len(description) > 2000:
            issues.append(f"Description too long: {len(description)}/2000 characters")

        if backend_keywords and len(backend_keywords) > 250:
            issues.append(f"Backend keywords too long: {len(backend_keywords)}/250 characters")

        return {
            "is_compliant": len(issues) == 0,
            "issues": issues
        }

    def get_forbidden_words(self) -> Dict[str, List[str]]:
        """Return the forbidden words for reference."""
        return {
            "forbidden": self.FORBIDDEN_WORDS,
        }

    def get_all_niches(self) -> List[str]:
        """Return all available niches."""
        return sorted(self.NICHE_DATA.keys())
