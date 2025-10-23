-- ---------------------------
-- Insert Categories
-- ---------------------------
INSERT INTO category (id, name, description) VALUES
(1, 'Sports', 'All types of sports activities'),
(2, 'Outdoor', 'Outdoor activities'),
(3, 'Relaxation', 'Leisure and relaxation activities');

-- ---------------------------
-- Insert Tags
-- ---------------------------
INSERT INTO tag (id, name, description) VALUES
(1, 'Morning', 'Best in the morning'),
(2, 'Evening', 'Best in the evening'),
(3, 'Group', 'Requires multiple participants'),
(4, 'Solo', 'Can be done alone');

-- ---------------------------
-- Insert Activities
-- ---------------------------
INSERT INTO activity 
(id, name, description, is_outdoor, is_groupe, intensity, duration, 
 ideal_temperature_min, ideal_temperature_max, weather_conditions, 
 location_type, min_age, max_age, accessibility_level, created_at, updated_at)
VALUES
(1, 'Hiking', 'Mountain hiking', true, true, 'medium', 180,
 15, 28, 'sunny', 'outdoor', 12, 60, 'moderate', NOW(), NOW()),
(2, 'Yoga', 'Indoor yoga session', false, false, 'low', 60,
 20, 25, 'sunny', 'indoor', 10, 70, 'easy', NOW(), NOW());

-- ---------------------------
-- Link Activities with Categories
-- ---------------------------
INSERT INTO activity_category (activity_id, category_id) VALUES
(1, 1),  -- Hiking -> Sports
(1, 2),  -- Hiking -> Outdoor
(2, 3);  -- Yoga -> Relaxation

-- ---------------------------
-- Link Activities with Tags
-- ---------------------------
INSERT INTO activity_tag (activity_id, tag_id) VALUES
(1, 1),  -- Hiking -> Morning
(1, 3),  -- Hiking -> Group
(2, 2),  -- Yoga -> Evening
(2, 4);  -- Yoga -> Solo