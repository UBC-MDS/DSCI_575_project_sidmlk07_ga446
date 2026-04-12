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
1. MBA Renewing Retinol Serum, 1.7 fl. oz, 0.5% Retinol Hydrates & Brightens Skin's Appearance by Dimin
2. Altaire Paris Anti Aging Intensive Youth Day Cream 1.7 Oz
3. Iryasa Night Indulge Cream - Natural Face Cream for Dry Skin - Vegan Anti Aging Night Cream for Wome
4. Dr. Au Anti-Aging Face Oil Retinol Serum by Au Natural Skinfood - Promotes Youthful, Glowing Skin
5. Origins High Potency Night-A-Mins Mineral-Enriched Moisture Cream 1.7oz, 50ml by Origins

**Semantic Search Top 5 Results:**
1. Ebanel 2.5% Retinol Serum for Face with Hyaluronic Acid, Peptide, Vitamin C, Pore Minimizer Skin Tig
2. Iryasa Night Indulge Cream - Natural Face Cream for Dry Skin - Vegan Anti Aging Night Cream for Wome
3. Iryasa Night Indulge Cream - Natural Face Cream for Dry Skin - Vegan Anti Aging Night Cream for Wome
4. APIVITA Queen Bee Holistic Age Defense Night Cream 1.69 fl.oz. |Intensive Night Treatment That Speed
5. MBA Renewing Retinol Serum, 1.7 fl. oz, 0.5% Retinol Hydrates & Brightens Skin's Appearance by Dimin

**Observations & Comparison:**
* **Which method performs better?** [Notes here]
* **Are there cases where BM25 fails but semantic search succeeds?** [Notes here]
* **Are the top results actually useful for the user’s intent?** [Notes here]

### Query 2: `body wash to help with rough bumpy skin on my arms` (Medium)
**BM25 Top 5 Results:**
1. Argus Le Waterproof Electric Facial and Body Cleansing Brush Facial Massager Natural Face Cleanser f
2. Hibiclens Antiseptic & Antimicrobial Skin Cleanser 32 Fl Oz (Pack of 2)
3. Juicy Chemistry - Organic & 100% Natural Hydrating Face & Body Scrub for Women with Dry & Mature Ski
4. Hylunia Hydrate Body Wash - Energizing Blend With Mango 8.5 oz
5. MYFOOT Moisturizing Foot Wipe for After Foot Mask Peel or After Beach, Fresh Cleansing Wet Wipes Hel

**Semantic Search Top 5 Results:**
1. Bath and Body Works 3 Pack Cocoshea Honey Softening Body Scrub 8 Oz.
2. Little Moon Essentials Tropical Bath & Shower Sugar Exfoliant, Beach All You Want, 2 oz.
3. Salux Nylon Japanese Beauty Skin Bath Wash Cloth/towel (3) Blue Yellow and Pink
4. Silk Exfoliating Mitt,Deep Exfoliating Mitt Body Scrub And Face Scrub,Dead Skin Removal Smooth Skin
5. Hemp Lotion for Dry Skin - Soothing Rose Flower & Aloe Hydrate Your Complexion - Non-Greasy, Vegan,

**Observations & Comparison:**
* **Which method performs better?** [Notes here]
* **Are there cases where BM25 fails but semantic search succeeds?** [Notes here]
* **Are the top results actually useful for the user’s intent?** [Notes here]

### Query 3: `luxury skincare travel kit gift for mom under $50` (Complex)
**BM25 Top 5 Results:**
1. 50th Birthday Gifts for Women, 40th Birthday Gifts Women, 60th Birthday Gifts for Women, Gift Basket
2. Frecia’s Allure Rose Quartz Face Roller Gua Sha Set – Brazilian Rose Quartz Gua Sha Stone Set with N
3. Bath Bombs Gift Set, Bath Bomb Gift for Women with Rose Petals, Lavender Scent 5pc Handmade Bubble B
4. Caudalie Favorites Set
5. GERSHION Pastel Gel Nail Polish Set, 6 Colors Gel Polish Set, Soak Off UV Lamp Gel Polish Kit, Nude

**Semantic Search Top 5 Results:**
1. Hanhoo Red pomegranate 6pcs Skin Care Set (6pcs/set)
2. EOS Delicate Petals & Blackberry Nectar Gift Set, pack of 1
3. Fragrantshare Makeup Brushes Professional Organizer Foundation Brush for Liquid makeup Travel 9Pcs S
4. Blackhead Mask,Sky-shop Facial Mask Nose Mask Face Mask Blackhead Cream with Activated Charcoal Deep
5. Face Moisturizer by Disco for Men, Hydrating, Anti-Aging Formula with Vitamin C, All Natural and Par

**Observations & Comparison:**
* **Which method performs better?** [Notes here]
* **Are there cases where BM25 fails but semantic search succeeds?** [Notes here]
* **Are the top results actually useful for the user’s intent?** [Notes here]

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
* **Which method performs better?** [Notes here]
* **Are there cases where BM25 fails but semantic search succeeds?** [Notes here]
* **Are the top results actually useful for the user’s intent?** [Notes here]

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
* **Which method performs better?** [Notes here]
* **Are there cases where BM25 fails but semantic search succeeds?** [Notes here]
* **Are the top results actually useful for the user’s intent?** [Notes here]

---

## 3. Summary of Insights

### A. Strengths and Weaknesses
**BM25:**
* **Strengths:** Excellent for Easy/Keyword queries (e.g., `vitamin c serum`). It guarantees exact term overlap, ensuring the user gets exactly the category they typed. 
* **Weaknesses:** Fails on Medium and Complex queries that use descriptive language, synonyms, or negative constraints (e.g., matching the word "break out" in a review, rather than finding a product that *prevents* breaking out).

**Semantic Search:**
* **Strengths:** Shines on Medium queries by capturing the underlying intent (e.g., understanding that "rough bumpy skin" maps to exfoliating products). 
* **Weaknesses:** Susceptible to "semantic drift." On Complex queries, the embeddings might average out the constraints, returning a highly relevant product type but completely missing a hard constraint like "under $20" or "cruelty-free."

### B. Challenging Queries for Both Methods
Both baseline methods struggle heavily with **Complex queries** that contain:
1. **Negations:** ("without white cast", "doesn't feel greasy")
2. **Subjectivity:** ("best", "highest rated")
3. **Hard Numerical Filters:** ("under $20", "over 50")

### C. Where Advanced Methods (RAG or Reranking) Would Help
* **Hybrid Search + Metadata Filtering:** Extracting entities (like Price < $20, or Brand) to use as hard filters *before* applying vector search would help solve the price constraint issues.
* **Cross-Encoder Reranking:** A reranker would better evaluate the relationship between all words in the complex queries, scoring a "tubing mascara" higher than a standard mascara, which standard bi-encoder embeddings often mix up.
* **RAG:** For highly specific queries (like the "luxury skincare gift"), an LLM could analyze the retrieved reviews to confirm if a product is actually well received as a gift, synthesizing a tailored recommendation.