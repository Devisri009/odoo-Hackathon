import { salaryInfos, SalaryInfo, SalaryComponent } from "../data/mockData";

let records = [...salaryInfos];

export const payrollService = {
  getByEmployee: async (employeeId: string): Promise<SalaryInfo | undefined> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return records.find(r => r.employeeId === employeeId);
  },

  updateSalaryInfo: async (employeeId: string, updates: Partial<SalaryInfo>): Promise<SalaryInfo> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const recordIndex = records.findIndex(r => r.employeeId === employeeId);
    
    if (recordIndex === -1) {
      // Create new
      const newRecord: SalaryInfo = {
        employeeId,
        monthWage: 0,
        yearlyWage: 0,
        workingDays: 22,
        workingSchedule: "Mon-Fri",
        breakTime: "1 Hour",
        wageType: "Fixed wage",
        pfRate: 12,
        professionalTax: 200,
        components: [],
        ...updates
      };
      records.push(newRecord);
      return newRecord;
    }
    
    records[recordIndex] = { ...records[recordIndex], ...updates };
    return records[recordIndex];
  },
  
  calculateComponentValue: (wage: number, component: SalaryComponent): number => {
    if (component.type === "PERCENTAGE") {
      return (wage * component.value) / 100;
    }
    return component.value;
  },
  
  calculateTotalSalary: (info: SalaryInfo): { gross: number, net: number, deductions: number } => {
    let gross = 0;
    info.components.forEach(c => {
      gross += payrollService.calculateComponentValue(info.monthWage, c);
    });
    
    const pfDeduction = (info.monthWage * info.pfRate) / 100;
    const deductions = pfDeduction + info.professionalTax;
    const net = gross - deductions;
    
    return { gross, net, deductions };
  }
};
