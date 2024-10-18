def summarize_issues(df):
    issues = []

    # Find the latest date in the 'date' column
    latest_date = df['date'].max()

    # Prepare a list to store the messages
    result_messages = []

    # Add the latest update date message
    result_messages.append(f"Latest data update: {latest_date.strftime('%d %B %Y')}\n")

    # Loop through each row in the dataframe
    for index, row in df.iterrows():
        # Check if any column violates the threshold
        problems = []

        if row['availability'] < 99.0:
            problems.append(f"low availability ({row['availability']:.2f})")

        if row['eut'] < 1.4:
            problems.append(f"low EUT ({row['eut']:.2f})")

        if row['traffic_gb'] < 300.0:
            problems.append(f"low traffic ({row['traffic_gb']:.2f})")

        if row['dl_prb'] < 93.0:
            problems.append(f"low PRB ({row['dl_prb']:.2f})")

        if problems:
            issue_summary = {
                'sector_id_hos': row['sector_id_hos'],
                'issues': problems
            }
            issues.append(issue_summary)
            
            # Add the issue messages to the result_messages list
            result_messages.append(f"Sector ID {issue_summary['sector_id_hos']} has issues:")
            for prob in issue_summary['issues']:
                result_messages.append(f" - {prob}")
            

    # If there are no issues
    if not issues:
        result_messages.append("No issues found.\n")

    # Join all the messages into a single string
    final_message = "\n".join(result_messages)

    # Print the final message once
    
    # Return the latest date and issues as a single variable (dictionary)
    return {
        'latest_update': latest_date.strftime('%d %B %Y'),
        'issues': issues,
        'message': final_message  # Include the final message in the return
    }
