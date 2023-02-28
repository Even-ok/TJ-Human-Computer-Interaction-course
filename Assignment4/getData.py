import pandas as pd

df_school_type = pd.read_csv(
    './college-salaries/salaries-by-college-type.csv')
df_school_region = pd.read_csv(
    './college-salaries/salaries-by-region.csv')
df_degree_payback = pd.read_csv(
    './college-salaries/degrees-that-pay-back.csv')


# Data processing, remove the '$' and ',' symbols in the data
def dataCleaning(df):
    ls = ['Starting Median Salary', 'Mid-Career Median Salary', 'Mid-Career 10th Percentile Salary',
          'Mid-Career 25th Percentile Salary', 'Mid-Career 75th Percentile Salary',
          'Mid-Career 90th Percentile Salary']
    for column in ls:
        for i in range(len(df[column])):
            if str(df[column][i]) != 'nan':
                df[column][i] = df[column][i][1:-1].replace(',', '').strip(" ")
    return df

# Get all possible school types
def get_school_types():
    return df_school_type['School Type'].unique()

# Get the school number dictionary corresponding to the school type
def get_school_types_value():
    tp_analysis = df_school_type["School Type"].value_counts()
    return tp_analysis

# Get all possible school districts
def get_school_regions():
    return df_school_region['Region'].unique()

# Get statistics for all possible school districts
def get_school_regions_value():
    tp_analysis = df_school_region["Region"].value_counts()
    return tp_analysis

# Return the major 
def get_undergraduate_major():
    return df_degree_payback['Undergraduate Major'].unique()

# Find the median salary of each stage according to the specific major
def get_media_salary_by_certain_major(major):
    available_major = get_undergraduate_major()
    dff = df_degree_payback.copy()
    dff = dff[dff['Undergraduate Major'] == major]
    salary = []
    for idx in range(4,8):
        salary.append(dff.iloc[0,idx])
    return salary

# Get a starting salary for each specific major (multiple choices)
def get_starting_salary_by_certain_major(major_list):
    # print(major_list)
    dff = df_degree_payback.copy()
    last_df = []
    if len(major_list)>0:
        last_df = dff[dff['Undergraduate Major'] == major_list[0]] # get first one
        for idx in range(1,len(major_list)):
            df2 = dff[dff['Undergraduate Major'] == major_list[idx]]
            last_df = last_df.append(df2,ignore_index=True)

    return last_df

# image salary_box data
def get_type_or_region_number(school_type_or_region):
    if school_type_or_region == 'Type':
        return get_school_types_value()
    else:
        return get_school_regions_value()

# Get statistics for all possible school districts
def get_regions_salary(region):
    dff = df_school_region.copy()
    dff = dff[dff['Region'] == region]
    return dff



def dataInit():
    global df_school_type, df_school_region,df_degree_payback
    df_school_type = dataCleaning(df_school_type)
    df_school_region = dataCleaning(df_school_region)
    df_degree_payback = dataCleaning(df_degree_payback)

if __name__ == '__main__':
    dataInit()