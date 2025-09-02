import { NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import { join } from 'path';
import { LenderConfig } from '../../types';

export async function GET() {
  try {
    const configPath = join(process.cwd(), '..', 'residential', 'lender_config.json');
    const configData = await readFile(configPath, 'utf-8');
    const config: LenderConfig = JSON.parse(configData);
    return NextResponse.json(config);
  } catch (error) {
    console.error('Failed to load lender config:', error);
    
    // Fallback configuration
    const fallbackConfig: LenderConfig = {
      lender_categories: {
        major_banks: ['hsbc_residential.txt', 'barclays_residential.txt', 'natwest_bank_residential.txt'],
        building_societies: ['halifax_bank_residential.txt', 'nationwide-residential.txt'],
        specialist_lenders: ['pepper_money_residential.txt', 'accord_residential.txt'],
        other_banks: ['santander_bank_residential.txt', 'virgin_money_residential.txt']
      }
    };
    
    return NextResponse.json(fallbackConfig);
  }
}
