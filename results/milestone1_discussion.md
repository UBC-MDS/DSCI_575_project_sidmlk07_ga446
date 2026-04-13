# Milestone 1 — Qualitative Evaluation: BM25 vs. Semantic Search

## 1. Query Set (Conversational Intent Progression)

| Theme | Easy | Medium | Complex |
| :--- | :--- | :--- | :--- |
| **1. Moisturizer** | `hydrating face moisturizer` | `lotion for skin that gets really dry in winter` | `what is the best fragrance-free moisturizer for sensitive skin under $30` |
| **2. Hair Frizz** | `argan oil hair serum` | `product to keep my hair from getting frizzy in the rain` | `best lightweight hair oil for thick curly hair that doesn't feel greasy` |
| **3. Sunscreen** | `mineral face sunscreen` | `sun protection that won't make me break out` | `what is a good daily sunscreen for dark skin tones that leaves no white cast` |
| **4. Anti-Aging** | `retinol night cream` | `something to help fade dark spots and wrinkles` | `highest rated anti-aging serum for women over 50` |
| **5. Color Care** | `purple shampoo` | `shampoo to stop my dyed hair from fading quickly` | `best sulfate-free shampoo for color treated hair under $15` |
| **6. Cleanser** | `salicylic acid face wash` | `cleanser to help get rid of blackheads and pimples` | `gentle morning face wash for acne prone teenage skin` |
| **7. Fragrance** | `vanilla eau de parfum` | `perfume that smells like fresh baked cookies` | `what is a long lasting evening fragrance for a date night` |
| **8. Concealer** | `under eye concealer` | `makeup to hide dark circles and look more awake` | `best hydrating concealer for mature skin that won't crease` |
| **9. Body Care** | `exfoliating body scrub` | `body wash to help with rough bumpy skin on my arms` | `what's a good chemical exfoliant for legs safe for daily use` |
| **10. Gifting** | `makeup brush set` | `good gift for someone who loves doing their makeup` | `luxury skincare travel kit gift for mom under $50` |

---

## 2. Results and Comparison for 5 Selected Queries

*(Note: The following 5 queries were selected from the table above to test a variety of retrieval challenges.)*

### Query 1: `retinol night cream` (Easy)
**BM25 Top 5 Results:**
1. Altaire Paris Anti Aging Intensive Youth Day Cream 1.7 Oz
2. MBA Renewing Retinol Serum, 1.7 fl. oz, 0.5% Retinol Hydrates & Brightens Skin's Appearance by Dimin
3. Iryasa Night Indulge Cream - Natural Face Cream for Dry Skin - Vegan Anti Aging Night Cream for Wome
4. Dr. Au Anti-Aging Face Oil Retinol Serum by Au Natural Skinfood - Promotes Youthful, Glowing Skin
5. Iryasa Night Indulge Cream - Natural Face Cream for Dry Skin - Vegan Anti Aging Night Cream for Wome

**Semantic Search Top 5 Results:**
1. Ebanel 2.5% Retinol Serum for Face with Hyaluronic Acid, Peptide, Vitamin C, Pore Minimizer Skin Tig
2. Iryasa Night Indulge Cream - Natural Face Cream for Dry Skin - Vegan Anti Aging Night Cream for Wome
3. Iryasa Night Indulge Cream - Natural Face Cream for Dry Skin - Vegan Anti Aging Night Cream for Wome
4. MBA Renewing Retinol Serum, 1.7 fl. oz, 0.5% Retinol Hydrates & Brightens Skin's Appearance by Dimin
5. APIVITA Queen Bee Holistic Age Defense Night Cream 1.69 fl.oz. |Intensive Night Treatment That Speed

**Observations & Comparison:**
- **Which method performs better?**
They perform similarly, but both struggle slightly to find a single product that combines all three terms perfectly in the title. Both return mainly relevant components (retinol serums and night creams).

- **Are there cases where BM25 fails but semantic search succeeds?**
BM25 failed on result #1 by returning a "Day Cream," simply because it keyword-matched "Cream". Semantic search avoided day creams, focusing strictly on night creams and serums.

- **Are the top results actually useful for the user’s intent?**
Mostly yes, both methods successfully identified the core active ingredient and the target application time.

### Query 2: `body wash to help with rough bumpy skin on my arms` (Medium)
**BM25 Top 5 Results:**
1. Argus Le Waterproof Electric Facial and Body Cleansing Brush Facial Massager Natural Face Cleanser f
2. Salux Nylon Japanese Beauty Skin Bath Wash Cloth/towel (3) Blue Yellow and Pink
3. MYFOOT Moisturizing Foot Wipe for After Foot Mask Peel or After Beach, Fresh Cleansing Wet Wipes Hel
4. Charcoal Konjac Face Sponge 3 pk | Acne, Psoriasis, Bumpy Skin & Ingrown Hairs
5. Way Of Will Sweet Orange Body Wash, Moisturizing Body Wash with Sweet Orange Essential Oil, Body Was

**Semantic Search Top 5 Results:**
1. Bath and Body Works 3 Pack Cocoshea Honey Softening Body Scrub 8 Oz.
2. Little Moon Essentials Tropical Bath & Shower Sugar Exfoliant, Beach All You Want, 2 oz.
3. Salux Nylon Japanese Beauty Skin Bath Wash Cloth/towel (3) Blue Yellow and Pink
4. Silk Exfoliating Mitt,Deep Exfoliating Mitt Body Scrub And Face Scrub,Dead Skin Removal Smooth Skin
5. Hemp Lotion for Dry Skin - Soothing Rose Flower & Aloe Hydrate Your Complexion - Non-Greasy, Vegan,

**Observations & Comparison:**
- **Which method performs better?**
Semantic search did much better at capturing the actual intent.

- **Are there cases where BM25 fails but semantic search succeeds?**
BM25 performed poorly by heavily weighting exact keywords ("wash", "body", "skin"). Because it lacks semantic understanding, it returned physical tools (a cleansing brush, a face sponge) and a foot wipe rather than a targeted treatment. Semantic search successfully decoded the underlying intent and matched the concept of "rough/bumpy skin" with exfoliating products.

- **Are the top results actually useful for the user’s intent?**
Semantic search's results are highly useful. A body scrub or exfoliating mitt is exactly what a user with rough, bumpy skin needs. BM25's results are mostly unhelpful, though Result #4 managed to string match "bumpy skin".

### Query 3: `luxury skincare travel kit gift for mom under $50` (Complex)
**BM25 Top 5 Results:**
1. 50th Birthday Gifts for Women, 40th Birthday Gifts Women, 60th Birthday Gifts for Women, Gift Basket
2. Frecia’s Allure Rose Quartz Face Roller Gua Sha Set – Brazilian Rose Quartz Gua Sha Stone Set with N
3. Caudalie Favorites Set
4. Bath Bombs Gift Set, Bath Bomb Gift for Women with Rose Petals, Lavender Scent 5pc Handmade Bubble B
5. Simple Pleasures 10-Piece Nail Polish Kit with Shimmering Nail Polish Shades, Glittery Toe Separator

**Semantic Search Top 5 Results:**
1. Hanhoo Red pomegranate 6pcs Skin Care Set (6pcs/set)
2. EOS Delicate Petals & Blackberry Nectar Gift Set, pack of 1
3. Fragrantshare Makeup Brushes Professional Organizer Foundation Brush for Liquid makeup Travel 9Pcs S
4. Blackhead Mask,Sky-shop Facial Mask Nose Mask Face Mask Blackhead Cream with Activated Charcoal Deep
5. Face Moisturizer by Disco for Men, Hydrating, Anti-Aging Formula with Vitamin C, All Natural and Par

**Observations & Comparison:**
- **Which method performs better?**
BM25 did better, while semantic search drifted heavily.

- **Are there cases where BM25 fails but semantic search succeeds?**
Semantic search suffered from severe drift, returning a makeup brush organizer, a blackhead mask, and a *men's* face moisturizer, completely ignoring the "mom" and "gift" intent. BM25 was able to anchor to the "gift" and "women" concepts.

- **Are the top results actually useful for the user’s intent?**
Most aren't great results, apart from the Caudalie set (BM25 #3). Notably, neither method understood the numerical price constraint. BM25 actually matched the "50" token to "50th Birthday Gifts" rather than interpreting it as a price, proving that text based retrieval cannot handle numerical logic without metadata filtering.

### Query 4: `mineral face sunscreen` (Easy)
**BM25 Top 5 Results:**
1. FASCY LAB GREEN+ Korean Sunscreen — SPF 50+PA++++, Daily Facial Sunscreen, Sun Cream With Patented I
2. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R
3. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R
4. Lesentia Tinted Moisturizer with SPF 31 – Tinted Moisturizer For Face With Spf and Blemish Concealer
5. DROP THE BOMB Bbosong Sun Stick SPF50+ PA++++ 15g - Oil Free UVA/UVB Protection Sebum Control Skin S

**Semantic Search Top 5 Results:**
1. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R
2. Pin Up Secret - Oil-Free Face Cream UVA/UVB - Protective Filter - Ideal for mixed to oily skins
3. Maquita Waterproof Portable Face Facial Highlighter Stick Shimmer Powder Makeup Silver
4. Hylunia Facial Day Lotion - 1.7 fl oz - Anti-Aging for Wrinkles - with Shea Butter, Hyaluronic Acid
5. Aloe Vera Gel 100% Natural Moisturisers - Pure Organic Fresh Soothing Aloe-Vera Moisturizing Gel Ski

**Observations & Comparison:**
* **Which method performs better?**
BM25 performs much better.

* **Are there cases where BM25 fails but semantic search succeeds?**
Some of the results of semantic search aren't even sunscreen, because it semantically drifted away.

* **Are the top results actually useful for the user’s intent?**
All the BM25 results are useful (all are sunscreen, even if not mineral), while a handful of semantic search ones are.

### Query 5: `what is a good daily sunscreen for dark skin tones that leaves no white cast` (Complex)
**BM25 Top 5 Results:**
1. FASCY LAB GREEN+ Korean Sunscreen — SPF 50+PA++++, Daily Facial Sunscreen, Sun Cream With Patented I
2. Lesentia Tinted Moisturizer with SPF 31 – Tinted Moisturizer For Face With Spf and Blemish Concealer
3. UNNY CLUB Cover Glow Cushion 0.3 Oz / 11g Beige Color SPF50+, Flawless Gloss Cushion Powder Complex
4. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R
5. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R

**Semantic Search Top 5 Results:**
1. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R
2. Pin Up Secret - Oil-Free Face Cream UVA/UVB - Protective Filter - Ideal for mixed to oily skins
3. XXI Skin | Bio-Pure Vitamin C Lotion | Provides 24 Hours of Hydration | Minimizes Fine Lines, Daily
4. So'Bio Étic | Moisturizing Fresh Gel Cream | Organic Face Moisturizer for Combination Skin | 24 hr H
5. [Abib] Creme coating mask Tone-up solution 17g (5pcs)

**Observations & Comparison:**
- **Which method performs better?**
BM25 did much better since it at least returned functional sunscreens with SPF. 

- **Are there cases where BM25 fails but semantic search succeeds?**
No, semantic performed poorly. It returned standard moisturizers without SPF, and actively failed the negative constraint ("no white cast") by returning a "Tone-up solution" mask (Semantic #5) which explicitly whitens the skin.

- **Are the top results actually useful for the user’s intent?**
Although the exact complex intent isn't perfectly satisfied by either, the BM25 results are safer and more relevant because they actually offer sun protection.

---

## 3. Summary of Insights

### A. Strengths and Weaknesses
**BM25:**
* **Strengths:** Excellent for Easy/Keyword queries (e.g., `mineral face sunscreen`). It guarantees exact term overlap, ensuring the user gets exactly the category they typed. Even on complex queries, it anchors well to the core nouns.
* **Weaknesses:** Fails entirely on Medium queries that use descriptive language or symptoms (e.g., searching for "rough bumpy skin" returns physical cleansing brushes and foot wipes instead of the necessary exfoliating body scrubs). It also misses negative constraints.

**Semantic Search:**
* **Strengths:** Does well on Medium queries by capturing the underlying intent. It successfully understood that a query about "rough bumpy skin" requires an exfoliating scrub or mitt.
* **Weaknesses:** Highly susceptible to *semantic drift*, sometimes even on simple queries. It can completely lose the core product category in favor of loosely related concepts (e.g., returning aloe gel instead of sunscreen, or a men's moisturizer for a "gift for mom"). It also blends constraints together rather than strictly enforcing them.

### B. Challenging Queries for Both Methods
Both baseline methods struggle heavily with Complex queries that contain:
1. **Negations:** (e.g., "no white cast"). Neither method understands that "no" modifies the next words. Semantic search even returned a tone up whitening mask, doing the exact opposite of the user's intent.
2. **Hard Numerical Filters:** (e.g., "under $50"). Neither method inherently understands price as a filter, prioritizing text matching instead.
3. **Multi-Faceted Intent:** Queries combining use cases, and subjective qualities (e.g., "luxury travel kit gift for mom") cause both models to not perform so well, usually failing to satisfy more than one of the conditions.

### C. Where Advanced Methods (RAG or Reranking) Would Help
* **Hybrid Search + Metadata Filtering:** Extracting entities (like Price < $50, or Brand) to use as hard filters *before* applying vector search would help solve the numerical constraint issues and keep results within budget.
* **Cross-Encoder Reranking:** A reranker would better evaluate the relationship between all words in the complex queries. It would penalize results that miss the core noun (reducing semantic drift).
* **RAG:** For highly specific queries (like the "luxury skincare gift"), an LLM could analyze the retrieved reviews to confirm if a product is actually well received as a gift by older women, synthesizing a tailored recommendation rather than just returning a list of products.