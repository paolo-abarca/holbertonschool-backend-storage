-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students --
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input --
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users
    SET average_score = (
	SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
        FROM corrections INNER JOIN
        projects ON projects.id = corrections.project_id
        WHERE corrections.user_id = user_id);
END $$
DELIMITER ;
