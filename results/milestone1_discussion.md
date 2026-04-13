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

1. Retinol Anti-aging Night Cream, Face Moisturizer for Anti-aging, Firming, Moisturizing With 3% Retin
2. Mererke_Pretty Retinol Cream, Moisturizing Cream for Face 1.7 Fl.Oz
3. Mererke_Pretty Retinol Cream, Moisturizing Cream for Face 1.7 Fl.Oz
4. Men's 2-Step Sensitive Skin Acne Cleanser & Face Cream Treatment Set - Face Wash + .05% Retinol = Cl
5. Men's 2-Step Sensitive Skin Acne Cleanser & Face Cream Treatment Set - Face Wash + .05% Retinol = Cl

**Semantic Search Top 5 Results:**

1. MBA Renewing Retinol Serum, 1.7 fl. oz, 0.5% Retinol Hydrates & Brightens Skin's Appearance by Dimin
2. Retinol 2.5% Cream From Majestic Pure for Face and Eye Area Will Nourish Your Skin, Potent Anti Agin
3. Mererke_Pretty Retinol Cream, Moisturizing Cream for Face 1.7 Fl.Oz
4. SOONPURE Retinol Eye Gel 84 g
5. Altaire Paris Anti Aging Intensive Youth Day Cream 1.7 Oz

**Observations & Comparison:**

- **Which method performs better?**

They perform similarly, but BM25 just about edged it, since it found a perfect match (#1). Both return mainly relevant components (retinol serums and night creams).

- **Are there cases where BM25 fails but semantic search succeeds?**

Semantic failed on result #5 by returning a "Day Cream," likely because it matched "Cream" with "anti-aging" (but ignored day/night).

- **Are the top results actually useful for the user’s intent?**

Yes, both methods successfully identified the core active ingredient (retinol). BM25's top result is the exact product requested. Semantic search consistently returned retinol products.

### Query 2: `body wash to help with rough bumpy skin on my arms` (Medium)

**BM25 Top 5 Results:**

1. Donell AHA 20 Face and Body Care Exfoliating Body Moisturizer Body Tingle
2. 100% Natural, Organic, Vegan Wet Skin Moisturizer for Dry Rough Bumpy Sensitive Skin: hydrate, repai
3. AmLactin Ultra Smoothing Intensely Hydrating Cream | Softens Rough, Bumpy Areas of Dry Skin | Powerf
4. Salux Super Hard Nylon Japanese Beauty Skin Bath Wash Cloth/towel (Grey)(Japan Import)
5. Aging Hippie Patchouli Aromatherapy Body Butter

**Semantic Search Top 5 Results:**

1. Way Of Will Sweet Orange Body Wash, Moisturizing Body Wash with Sweet Orange Essential Oil, Body Was
2. Bath and Body Works 3 Pack Cocoshea Honey Softening Body Scrub 8 Oz.
3. Hylunia Hydrate Body Wash - Energizing Blend With Mango 8.5 oz
4. Baebody Coconut Milk Body Scrub: With Dead Sea Salt, Almond Oil, and Vitamin E. - Exfoliator, Moistu
5. Tropic Labs White Sands Dual-Action Body Scrub | Natural Exfoliating Body Scrubs | Gentle Exfoliator

**Observations & Comparison:**

- **Which method performs better?**

Semantic search did much better at capturing the actual intent.

- **Are there cases where BM25 fails but semantic search succeeds?**

BM25 performed poorly by heavily weighting exact keywords ("wash", "body", "skin"). Because it lacks semantic understanding, it returned lotions and creams rather than a targeted treatment. Semantic search successfully decoded the underlying intent and matched the concept of "rough/bumpy skin" with exfoliating products.

- **Are the top results actually useful for the user’s intent?**

Semantic search's results are highly useful. A body scrub or exfoliating mitt is exactly what a user with rough, bumpy skin needs. BM25's results are not that unhelpful (more cream/lotion type).

### Query 3: `luxury skincare travel kit gift for mom under $50` (Complex)

**BM25 Top 5 Results:**

1. 50th Birthday Gifts for Women, 40th Birthday Gifts Women, 60th Birthday Gifts for Women, Gift Basket
2. Caudalie Favorites Set
3. Manicure Set，Nail clipper set 16 in 1， Women Grooming kit, with luxury pink leather case, family and
4. Dr. August Wolff GmbH & Co.KG Arzneimittel LINOLA Schutz-Balsam 50 ml (1 x 50 ml)
5. 50th Birthday Gifts for Women, 40th Birthday Gifts Women, 60th Birthday Gifts for Women, Gift Basket

**Semantic Search Top 5 Results:**

1. Facial Kit For Women - Includes Facial Mask, Facial Makeup Wipes, Nose Strips, Facial Cleansers, Fac
2. go1go Bath Bombs Gift Set, 6 Pack Natural Rich in Essential Oils Spa Bath Fizzies for Moisturizing D
3. BeautyStat Mini Universal Essentials Skin Care Kit - 3 in 1: Universal C Skin Refiner + Universal Pr
4. NeWisdom 72 PCS Toddler Girls Hair Accessory Set with Gift Packing Organization Box, Gifts for Grand
5. NeWisdom 72 PCS Toddler Girls Hair Accessory Set with Gift Packing Organization Box, Gifts for Grand

**Observations & Comparison:**

- **Which method performs better?**

BM25 did slightly better since it anchored to "gift", but overall, both methods struggled with the complexity.

- **Are there cases where BM25 fails but semantic search succeeds?**

Semantic search suffered from severe drift (#4 and #5), returning a "Toddler Girls Hair Accessory Set" simply because it contained the word "Gifts."

- **Are the top results actually useful for the user’s intent?**

Most are not great. Notably, neither method understood the numerical price constraint ("under $50"). BM25 matched the "50" token as literal text, returning "50th Birthday Gifts" and a lotion with "50 ml".

### Query 4: `mineral face sunscreen` (Easy)

**BM25 Top 5 Results:**

1. Mineral Sun Block by Disco for Men, Moisturizing, SPF 30, All Natural and Paraben Free, 2 Ounces
2. Alteya Organics Sunscreen Rose Face Cream Spf 30, 50 ML
3. FASCY LAB GREEN+ Korean Sunscreen — SPF 50+PA++++, Daily Facial Sunscreen, Sun Cream With Patented I
4. SHISEIDO ANESSA Perfect UV Sunscreen Mild Milk N SPF50+ PA++++ 60ml
5. Hang Ten - Classic Face Natural Sunscreen Lotion 30 SPF - 3 oz.

**Semantic Search Top 5 Results:**

1. Mineral Sun Block by Disco for Men, Moisturizing, SPF 30, All Natural and Paraben Free, 2 Ounces
2. FASCY LAB GREEN+ Korean Sunscreen — SPF 50+PA++++, Daily Facial Sunscreen, Sun Cream With Patented I
3. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R
4. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R
5. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R

**Observations & Comparison:**

- **Which method performs better?**
BM25 performs much better, by offering a wider, more accurate variety of products specifically designed for the face.

- **Are there cases where BM25 fails but semantic search succeeds?**

No. Semantic did return more generic results though.

- **Are the top results actually useful for the user’s intent?**

Both methods are useful because they all return sunscreens with SPF. However, BM25 better does better with the "face" constraint.

### Query 5: `what is a good daily sunscreen for dark skin tones that leaves no white cast` (Complex)

**BM25 Top 5 Results:**

1. FASCY LAB GREEN+ Korean Sunscreen — SPF 50+PA++++, Daily Facial Sunscreen, Sun Cream With Patented I
2. Lesentia Tinted Moisturizer with SPF 31 – Tinted Moisturizer For Face With Spf and Blemish Concealer
3. UNNY CLUB Cover Glow Cushion 0.3 Oz / 11g Beige Color SPF50+, Flawless Gloss Cushion Powder Complex
4. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R
5. Coppertone Kids Clear Sunscreen Lotion SPF 50, Water Resistant Sunscreen for Kids, #1 Pediatrician R

**Semantic Search Top 5 Results:**

1. Mineral Sun Block by Disco for Men, Moisturizing, SPF 30, All Natural and Paraben Free, 2 Ounces
2. Hang Ten - Classic Face Natural Sunscreen Lotion 30 SPF - 3 oz.
3. FASCY LAB GREEN+ Korean Sunscreen — SPF 50+PA++++, Daily Facial Sunscreen, Sun Cream With Patented I
4. Alteya Organics Sunscreen Rose Face Cream Spf 30, 50 ML
5. Darksyde Ultra Bronze Self Tanning Lotion, 8.5 ounces

**Observations & Comparison:**

- **Which method performs better?**

BM25 did much since all the results are at least functional sunscreens with SPF. #5 for semantic isn't even sunscreen.

- **Are there cases where BM25 fails but semantic search succeeds?**

No, Semantic Search actually failed on #5. By trying to interpret "dark skin tones," it semantically drifted into returning a "Self Tanning Lotion" product, completely missing the fact that the user is seeking SPF.

- **Are the top results actually useful for the user’s intent?**

BM25's results are safer and more relevant because they actually offer sun protection. However, both methods fail the negative constraint ("no white cast"), as neither retrieval model understands that the word "no" negates the terms that follow it.

---

## 3. Summary of Insights

### A. Strengths and Weaknesses

**BM25:**

- **Strengths:** Excellent for Easy/Keyword queries (e.g., `mineral face sunscreen`). It guarantees exact term overlap, ensuring the user gets exactly the category they typed. Even on complex queries, it anchors well to the core nouns.
- **Weaknesses:** Fails entirely on Medium queries that use descriptive language or symptoms (e.g., searching for a "body wash" for "rough bumpy skin" returns leave-on moisturizers and hydrating creams instead of the necessary in-shower wash). It also completely misses negative constraints.

**Semantic Search:**

- **Strengths:** Does well on Medium queries by capturing the underlying intent. It successfully understood that a query about "rough bumpy skin" requires an exfoliating scrub or wash, decoding the problem into a solution.

- **Weaknesses:** Highly susceptible to severe *semantic drift*, sometimes even on simple queries. It can completely lose the core product category in favor of loosely related concepts (e.g., returning a self-tanning bronzer instead of sunscreen, or a toddler's hair accessory set for a "gift for mom"). It also blends constraints together rather than strictly enforcing them.

### B. Challenging Queries for Both Methods

Both baseline methods struggle heavily with Complex queries that contain:

1. **Negations:** (e.g., "no white cast"). Neither method understands that "no" modifies the next words. Semantic search even returned a tone up whitening mask, doing the exact opposite of the user's intent.
2. **Hard Numerical Filters:** (e.g., "under $50"). Neither method inherently understands price as a filter, prioritizing text matching instead.
3. **Multi-Faceted Intent:** Queries combining use cases, and subjective qualities (e.g., "luxury travel kit gift for mom") cause both models to not perform so well, usually failing to satisfy more than one of the conditions.

### C. Where Advanced Methods (RAG or Reranking) Would Help

- **Hybrid Search + Metadata Filtering:** Extracting entities (like Price < $50, or Brand) to use as hard filters *before* applying vector search would help solve the numerical constraint issues and keep results within budget.
- **Cross-Encoder Reranking:** A reranker would better evaluate the relationship between all words in the complex queries. It would penalize results that miss the core noun (reducing semantic drift).
- **RAG:** For highly specific queries (like the "luxury skincare gift"), an LLM could analyze the retrieved reviews to confirm if a product is actually well received as a gift by older women, synthesizing a tailored recommendation rather than just returning a list of products.