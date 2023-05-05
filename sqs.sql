alter TABLE `diemdanhdb`.`student` (
    `dep` VARCHAR(45) NULL,
    `course` VARCHAR(45) NULL,
    `year` VARCHAR(45) NULL,
    `semester` VARCHAR(45) NULL,
    `studentID` int NOT NULL,
    `name` VARCHAR(45) NULL,
    `division` VARCHAR(45) NULL,
    `Roll` VARCHAR(45) NULL,
    `gender` VARCHAR(45) NULL,
    `Dob` VARCHAR(45) NULL,
    `mail` VARCHAR(45) NULL,
    `phone` VARCHAR(45) NULL,
    `Address` VARCHAR(45) NULL,
    `teacher` VARCHAR(45) NULL,
    `photoSample` VARCHAR(45) NULL,
    PRIMARY KEY (`studentID`)
  );