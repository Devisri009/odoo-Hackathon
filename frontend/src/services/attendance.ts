import { attendanceRecords, AttendanceRecord } from "../data/mockData";

// Keep a mutable local copy to simulate a database for the current session
let records = [...attendanceRecords];

export const attendanceService = {
  getByEmployee: async (employeeId: string): Promise<AttendanceRecord[]> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return records.filter(r => r.employeeId === employeeId);
  },

  getAll: async (): Promise<AttendanceRecord[]> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return records;
  },

  checkIn: async (employeeId: string): Promise<AttendanceRecord> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const now = new Date();
    const timeString = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    const dateString = now.toISOString().split('T')[0];
    
    const newRecord: AttendanceRecord = {
      id: `att_${Date.now()}`,
      employeeId,
      date: dateString,
      checkIn: timeString,
      checkOut: null,
      workHours: 0,
      extraHours: 0
    };
    
    records = [newRecord, ...records];
    return newRecord;
  },

  checkOut: async (recordId: string): Promise<AttendanceRecord | null> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const recordIndex = records.findIndex(r => r.id === recordId);
    if (recordIndex === -1) return null;
    
    const now = new Date();
    const timeString = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    
    // Simple mock calculation for work hours
    const checkInHour = parseInt(records[recordIndex].checkIn.split(':')[0]);
    const checkOutHour = now.getHours();
    const workHours = checkOutHour - checkInHour;
    
    const updatedRecord = {
      ...records[recordIndex],
      checkOut: timeString,
      workHours: workHours > 0 ? workHours : 0
    };
    
    records[recordIndex] = updatedRecord;
    return updatedRecord;
  }
};
