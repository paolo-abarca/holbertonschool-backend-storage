-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student --
-- Procedure ComputeAverageScoreForUser is taking 1 input: --
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
    IN user_id INT
)
BEGIN
    UPDATE users
    SET average_score = (SELECT SUM(score * weight) / SUM(weight) 
	FROM corrections INNER JOIN
	projects ON corrections.project_id = projects.id
	WHERE corrections.user_id = user_id)
    WHERE id = user_id;
END $$
DELIMITER ;
