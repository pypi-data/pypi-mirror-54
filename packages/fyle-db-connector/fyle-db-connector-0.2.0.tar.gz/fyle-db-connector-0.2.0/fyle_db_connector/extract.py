"""
FyleExtractConnector(): Connection between Fyle and Database
"""

import logging
from typing import List

import pandas as pd
from fylesdk import FyleSDK

logger = logging.getLogger('FyleConnector')


class FyleExtractConnector:
    """
    - Extract Data from Fyle and load to Database
    """
    def __init__(self, fyle_config, database):
        self.__database = database

        self.__connection = FyleSDK(
            base_url=fyle_config.get('fyle_base_url'),
            client_id=fyle_config.get('fyle_client_id'),
            client_secret=fyle_config.get('fyle_client_secret'),
            refresh_token=fyle_config.get('fyle_refresh_token')
        )
        logger.info('Fyle connection established.')

    def extract_settlements(self, updated_at: List['str'] = None, exported: bool = None) -> List[str]:
        """
        Extract settlements from Fyle
        :param updated_at: Date string in yyyy-MM-ddTHH:mm:ss.SSSZ format along with operator in RHS colon pattern.
        :param exported: True for exported settlements and False for unexported settlements
        :return: List of settlement ids
        """

        logger.info('Extracting settlements from Fyle.')

        settlements = self.__connection.Settlements.get_all(updated_at=updated_at, exported=exported)

        df_settlements = pd.DataFrame(settlements)
        logger.info('%s settlements extracted.', str(len(df_settlements.index)))

        if settlements:
            df_settlements.to_sql('settlements', self.__database.connection, if_exists='replace', index=False)
            return df_settlements['id'].to_list()

        return []

    def extract_employees(self) -> List[str]:
        """
        Extract employees from Fyle
        :return: List of employee ids
        """

        logger.info('Extracting employees from Fyle.')
        employees = self.__connection.Employees.get_all()

        logger.info('%s employees extracted.', str(len(employees)))

        if employees:
            df_employees = pd.DataFrame(employees)

            df_employees['custom_fields'] = df_employees['custom_fields'].astype('str')
            df_employees['mileage_rate_labels'] = df_employees['mileage_rate_labels'].astype('str')
            df_employees['annual_mileage_of_user_before_joining_fyle'] = df_employees[
                'annual_mileage_of_user_before_joining_fyle'].astype('str')
            df_employees['perdiem_names'] = df_employees['perdiem_names'].astype('str')

            df_employees.to_sql('employees', self.__database.connection, if_exists='replace', index=False)
            return df_employees['id'].to_list()

        return []

    def extract_expenses(self, settlement_ids: List[str] = None, state: List[str] = None,
                         fund_source: List[str] = None, reimbursable: bool = None,
                         exported: bool = None) -> List[str]:
        """
        Extract expenses from Fyle
        :param exported: True for exported expenses and False for unexported expenses
        :param settlement_ids: List of settlement_ids
        :param state: List of expense states
        :param fund_source: List of expense fund_sources
        :param reimbursable: True for reimbursable expenses, False for non reimbursable expenses
        :return: List of expense ids
        """

        logger.info('Extracting expenses from Fyle.')

        expenses = self.__connection.Expenses.get_all(
            settlement_id=settlement_ids,
            state=state,
            fund_source=fund_source,
            exported=exported
        )

        if reimbursable is not None:
            expenses = list(filter(lambda expense: expense['reimbursable'], expenses))

        logger.info('%s expenses extracted.', str(len(expenses)))

        if expenses:
            df_expenses = pd.DataFrame(expenses)

            df_expenses['approved_by'] = df_expenses['approved_by'].map(lambda expense: expense[0] if expense else None)
            df_expenses['approved_by'] = df_expenses['approved_by'].astype('str')
            df_expenses['export_ids'] = df_expenses['export_ids'].astype('str')
            df_expenses['custom_properties'] = df_expenses['custom_properties'].astype('str')
            df_expenses['locations'] = df_expenses['locations'].astype('str')

            df_expenses.to_sql('expenses', self.__database.connection, if_exists='replace', index=False)

            return df_expenses['id'].to_list()

        return []

    def extract_attachments(self, expense_ids: List[str]) -> List[str]:
        """
        Extract attachments from Fyle
        :param expense_ids: List of Expense Ids
        :return: List of expense ids for which attachments were downloaded
        """
        attachments = []

        logger.info('Extracting attachments from Fyle')

        if expense_ids:
            for expense_id in expense_ids:
                attachment = self.__connection.Expenses.get_attachments(expense_id)
                if attachment['data']:
                    attachment = attachment['data'][0]
                    attachment['expense_id'] = expense_id
                    attachments.append(attachment)

            logger.info('%s attachments extracted.', str(len(attachments)))

            if attachments:
                df_attachments = pd.DataFrame(attachments)
                df_attachments.to_sql('attachments', self.__database.connection, if_exists='replace', index=False)
                return df_attachments['expense_id'].to_list()

        logger.info('0 attachments extracted.')
        return []

    def extract_categories(self) -> List[str]:
        """
        Extract categories from Fyle
        :return: List of category ids
        """
        logger.info('Extracting categories from Fyle.')

        categories = self.__connection.Categories.get()['data']

        logger.info('%s categories extracted.', str(len(categories)))

        if categories:
            df_categories = pd.DataFrame(categories)
            df_categories.to_sql('categories', self.__database.connection, if_exists='replace', index=False)
            return df_categories['id'].to_list()

        return []

    def extract_projects(self) -> List[str]:
        """
        Extract projects from Fyle
        :return: List of project ids
        """
        logger.info('Extracting categories from Fyle.')

        projects = self.__connection.Projects.get()['data']

        logger.info('%s projects extracted.', str(len(projects)))

        if projects:
            df_projects = pd.DataFrame(projects)
            df_projects.to_sql('projects', self.__database.connection, if_exists='replace', index=False)
            return df_projects['id'].to_list()

        return []

    def extract_cost_centers(self) -> List[str]:
        """
        Extract cost centers from Fyle
        :return: List of cost center ids
        """
        logger.info('Extracting categories from Fyle.')

        cost_centers = self.__connection.CostCenters.get(False)['data']

        logger.info('%s cost centers extracted.', str(len(cost_centers)))

        if cost_centers:
            df_cost_centers = pd.DataFrame(cost_centers)
            df_cost_centers.to_sql('cost_centers', self.__database.connection, if_exists='replace', index=False)
            return df_cost_centers['id'].to_list()

        return []

    def extract_reimbursements(self, state: List[str] = None, exported: bool = None) -> List[str]:
        """
        Extract reimbursements from Fyle
        :param state: List of states
        :param exported: True for exported reimbursements and False for unexeported reimbursements
        :return: List of reimbursement ids
        """
        logger.info('Extracting reimbursements from Fyle.')
        reimbursements = self.__connection.Reimbursements.get_all()

        if state:
            reimbursements = list(filter(
                lambda reimbursement: reimbursement['state'] in state,
                reimbursements
            ))

        if exported:
            reimbursements = list(filter(
                lambda reimbursement: reimbursement['exported'] == exported,
                reimbursements
            ))

        logger.info('%s reimbursements extracted.', str(len(reimbursements)))

        if reimbursements:
            df_reimbursements = pd.DataFrame(reimbursements)
            df_reimbursements['export_ids'] = df_reimbursements['export_ids'].astype('str')
            df_reimbursements.to_sql('reimbursements', self.__database.connection, if_exists='replace', index=False)
            return df_reimbursements['id'].to_list()

        return []

    def extract_advances(self, settlement_ids: List[str] = None) -> List[str]:
        """
        Extract advances from Fyle
        :param settlement_ids: List of settlement ids
        :return: List of advance ids
        """
        logger.info('Extracting advances from Fyle.')
        advances = self.__connection.Advances.get_all(
            settlement_id=settlement_ids
        )

        logger.info('%s advances extracted.', str(len(advances)))

        if advances:
            df_advances = pd.DataFrame(advances)

            df_advances['export_ids'] = df_advances['export_ids'].astype('str')
            df_advances['approved_by'] = df_advances['approved_by'].astype('str')

            df_advances.to_sql('advances', self.__database.connection, if_exists='replace', index=False)
            return df_advances['id'].to_list()

        return []

    def extract_advance_requests(self, state: List[str] = None, updated_at: List[str] = None,
                                 exported: bool = None) -> List[str]:
        """
        Extract advance requests from Fyle
        :param state:
        :param updated_at:
        :param exported:
        :return: List of advance request ids
        """
        logger.info('Extracting advance requests from Fyle.')

        advance_requests = self.__connection.AdvanceRequests.get_all(
            state=state,
            updated_at=updated_at,
            exported=exported
        )

        logger.info('%s advance requests extracted.', str(len(advance_requests)))

        if advance_requests:
            df_advance_requests = pd.DataFrame(advance_requests)

            df_advance_requests['export_ids'] = df_advance_requests['export_ids'].astype('str')
            df_advance_requests['approved_by'] = df_advance_requests['approved_by'].astype('str')

            if len(df_advance_requests['custom_field_values'].index):
                advance_request_custom_fields = []

                for row in df_advance_requests.to_dict(orient='records'):
                    custom_field = {}
                    custom_fields = row['custom_field_values']
                    custom_field['advance_request_id'] = row['id']

                    for field in custom_fields:
                        custom_field[field['name']] = field['value']

                    advance_request_custom_fields.append(custom_field)

                df_advance_requests_custom_fields = pd.DataFrame(advance_request_custom_fields)
                df_advance_requests_custom_fields.to_sql(
                    'advance_request_custom_fields',
                    self.__database.connection,
                    if_exists='replace',
                    index=False
                )

            df_advance_requests['custom_field_values'] = df_advance_requests['custom_field_values'].astype('str')

            df_advance_requests.to_sql('advance_requests', self.__database.connection, if_exists='replace', index=False)

            return df_advance_requests['id'].to_list()
        return []
