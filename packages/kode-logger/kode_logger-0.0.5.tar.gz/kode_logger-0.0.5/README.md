# KODE Logger

## Usage example
```python
import kode_logger

logger = kode_logger.create_json('my-app-context')
logger.warning('some_message', extra={
    'custom_variable': 'value'
})
```
