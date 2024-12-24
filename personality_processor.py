# personality_processor.py
import pandas as pd

def generate_personalized_quotes(df_staff_id_1, top_traits_file, low_traits_file):
    # Count and sort responses
    response_counts = pd.concat([
        df_staff_id_1['Response_1'], 
        df_staff_id_1['Response_2'], 
        df_staff_id_1['Response_3'],
        df_staff_id_1['Response_4'], 
        df_staff_id_1['Response_5']
    ]).value_counts()

    # Top 3 traits
    top_3_traits = response_counts.index[:3].tolist()

    # Bottom 3 traits
    bottom_3_traits = response_counts.index[-3:].tolist()

    # Find matching quote for top 3 traits
    df_top_quotes = pd.read_csv(top_traits_file)
    matching_top_quotes = df_top_quotes[
        (df_top_quotes['Trait 1'].isin(top_3_traits)) & 
        (df_top_quotes['Trait 2'].isin(top_3_traits)) & 
        (df_top_quotes['Trait 3'].isin(top_3_traits))
    ]

    top_quote = "No matching quote found for the top traits."
    if not matching_top_quotes.empty:
        top_quote = matching_top_quotes['Quote'].iloc[0]

    # Find matching quote for bottom 3 traits
    df_low_quotes = pd.read_csv(low_traits_file)
    matching_low_quotes = df_low_quotes[
        (df_low_quotes['trait_1'].isin(bottom_3_traits)) & 
        (df_low_quotes['trait_2'].isin(bottom_3_traits)) & 
        (df_low_quotes['trait_3'].isin(bottom_3_traits))
    ]

    low_quote = "No matching quote found for the bottom traits."
    if not matching_low_quotes.empty:
        low_quote = matching_low_quotes['quotes'].iloc[0]

    # Replace placeholder with teacher's name
    teacher_counts = df_staff_id_1['staff_name'].value_counts()
    teacher = teacher_counts.idxmax()
    top_quote = top_quote.replace("[This teacher]", teacher)
    low_quote = low_quote.replace("[This teacher]", teacher)

    return top_quote, low_quote

def process_personality_data(input_file, output_file):
    df = pd.read_csv(input_file)
    staff_ids = df['staff_id'].unique()
    split_dfs = {}

    for staff_id in staff_ids:
        df_filtered = df[df['staff_id'] == staff_id]
        split_dfs[staff_id] = pd.DataFrame({
            'staff_name': df_filtered['staff_name'],
            'Response_1': df_filtered['Response_1'],
            'Response_2': df_filtered['Response_2'],
            'Response_3': df_filtered['Response_3'], 
            'Response_4': df_filtered['Response_4'],
            'Response_5': df_filtered['Response_5']
        })

    top_traits_file = 'Top_traits.csv'
    low_traits_file = 'Low_traits.csv'
    results = []

    for staff_id in staff_ids:
        df_staff_id_1 = split_dfs[staff_id]
        top_quote, low_quote = generate_personalized_quotes(df_staff_id_1, top_traits_file, low_traits_file)
        results.append({'staff_id': staff_id, 'top_quote': top_quote, 'low_quote': low_quote})

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)

    print(f"Output saved to {output_file}")
