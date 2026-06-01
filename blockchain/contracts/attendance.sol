// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Attendance {

    address public owner;

    struct Student {
        string name;
        string srn;
        bool registered;
    }

    struct AttendanceRecord {
        string srn;
        string subject;
        uint256 timestamp;
        bool present;
        string locationHash;
    }

    // SRN => Student
    mapping(string => Student) public students;

    // SRN => list of attendance records
    mapping(string => AttendanceRecord[]) public attendanceRecords;

    // Duplicate check: SRN => subject => date => already marked?
    mapping(string => mapping(string => mapping(string => bool))) public alreadyMarked;

    // Last marked timestamp for any subject: SRN => timestamp
    mapping(string => uint256) public lastMarkedTime;

    // 45 minutes in seconds
    uint256 public constant MIN_GAP = 45 * 60;

    // All registered SRNs
    string[] public allSRNs;

    // Events
    event StudentRegistered(string srn, string name);
    event AttendanceMarked(string srn, string subject, uint256 timestamp);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    // Register a new student
    function registerStudent(string memory _srn, string memory _name) public onlyOwner {
        require(!students[_srn].registered, "Student already registered");
        students[_srn] = Student(_name, _srn, true);
        allSRNs.push(_srn);
        emit StudentRegistered(_srn, _name);
    }

    // Mark attendance with duplicate + 45 min gap check
    function markAttendance(
        string memory _srn,
        string memory _subject,
        string memory _date,
        string memory _locationHash
    ) public onlyOwner {
        require(students[_srn].registered, "Student not registered");

        // Check: same subject same day duplicate
        require(
            !alreadyMarked[_srn][_subject][_date],
            "Attendance already marked for this subject today"
        );

        // Check: 45 min gap from last attendance in ANY subject
        if (lastMarkedTime[_srn] != 0) {
            require(
                block.timestamp >= lastMarkedTime[_srn] + MIN_GAP,
                "Too soon: wait 45 minutes between subjects"
            );
        }

        alreadyMarked[_srn][_subject][_date] = true;
        lastMarkedTime[_srn] = block.timestamp;

        AttendanceRecord memory record = AttendanceRecord({
            srn: _srn,
            subject: _subject,
            timestamp: block.timestamp,
            present: true,
            locationHash: _locationHash
        });
        attendanceRecords[_srn].push(record);
        emit AttendanceMarked(_srn, _subject, block.timestamp);
    }

    // Check duplicate for today
    function hasMarkedToday(
        string memory _srn,
        string memory _subject,
        string memory _date
    ) public view returns (bool) {
        return alreadyMarked[_srn][_subject][_date];
    }

    // Get seconds remaining before student can be marked again (0 = can mark now)
    function timeUntilNextMark(string memory _srn) public view returns (uint256) {
        if (lastMarkedTime[_srn] == 0) return 0;
        uint256 nextAllowed = lastMarkedTime[_srn] + MIN_GAP;
        if (block.timestamp >= nextAllowed) return 0;
        return nextAllowed - block.timestamp;
    }

    // Get total attendance count for a student in a subject
    function getAttendanceCount(string memory _srn, string memory _subject)
        public view returns (uint256)
    {
        uint256 count = 0;
        AttendanceRecord[] memory records = attendanceRecords[_srn];
        for (uint i = 0; i < records.length; i++) {
            if (keccak256(bytes(records[i].subject)) == keccak256(bytes(_subject))) {
                count++;
            }
        }
        return count;
    }

    // Get all attendance records for a student
    function getStudentRecords(string memory _srn)
        public view returns (AttendanceRecord[] memory)
    {
        return attendanceRecords[_srn];
    }

    // Get total number of registered students
    function getTotalStudents() public view returns (uint256) {
        return allSRNs.length;
    }

    // Check if student is registered
    function isRegistered(string memory _srn) public view returns (bool) {
        return students[_srn].registered;
    }
}
